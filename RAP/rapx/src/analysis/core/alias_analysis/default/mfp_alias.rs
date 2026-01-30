use super::graph::MopGraph;
use rustc_data_structures::fx::{FxHashMap, FxHashSet};
use rustc_middle::mir::{Operand, TerminatorKind};
use std::collections::VecDeque;
use std::time::{Duration, Instant};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AbstractState {
    pub alias_sets: Vec<FxHashSet<usize>>,
    pub constants: FxHashMap<usize, usize>,
    pub path: Vec<usize>,
    pub iter_count: usize,
}

impl AbstractState {
    pub fn new() -> Self {
        AbstractState {
            alias_sets: Vec::new(),
            constants: FxHashMap::default(),
            path: Vec::new(),
            iter_count: 0,
        }
    }

    pub fn snapshot(graph: &MopGraph) -> Self {
        AbstractState {
            alias_sets: graph.alias_sets.clone(),
            constants: graph.constants.clone(),
            path: Vec::new(),
            iter_count: 0,
        }
    }

    pub fn restore_to(&self, graph: &mut MopGraph) {
        graph.alias_sets = self.alias_sets.clone();
        graph.constants = self.constants.clone();
    }
}

#[derive(Clone, Debug)]
pub struct ConstraintContext {
    pub constraints: FxHashMap<usize, usize>,
}

impl ConstraintContext {
    pub fn new() -> Self {
        ConstraintContext {
            constraints: FxHashMap::default(),
        }
    }
}

#[derive(Clone, Debug)]
pub struct Slice {
    pub start_node: usize,
    pub end_node: usize,
    pub blocks: Vec<usize>,
    pub is_exit: bool,
}

#[derive(Debug, Clone)]
pub struct SccMetadata {
    pub id: usize,
    pub dominator: usize,
    pub exits: Vec<usize>,
    pub back_edges: Vec<usize>,
    pub nodes: Vec<usize>,
    pub sub_sccs: Vec<SccMetadata>,
}

pub struct HierarchicalAnalyzer<'a, 'tcx> {
    pub graph: &'a mut MopGraph<'tcx>,
    pub scc_tree: Vec<SccMetadata>,
    pub dom_to_scc: FxHashMap<usize, SccMetadata>,
    pub summary_cache: Vec<(usize, AbstractState, Vec<(usize, AbstractState)>)>,
    pub time_decomp: Duration,
    pub time_constraint: Duration,
    pub time_alias: Duration,
    pub time_path_synth: Duration,
    pub time_total: Duration,
}

impl<'a, 'tcx> HierarchicalAnalyzer<'a, 'tcx> {
    pub fn new(graph: &'a mut MopGraph<'tcx>) -> Self {
        HierarchicalAnalyzer {
            graph,
            scc_tree: Vec::new(),
            dom_to_scc: FxHashMap::default(),
            summary_cache: Vec::new(),
            time_decomp: Duration::new(0, 0),
            time_constraint: Duration::new(0, 0),
            time_alias: Duration::new(0, 0),
            time_path_synth: Duration::new(0, 0),
            time_total: Duration::new(0, 0),
        }
    }
}

impl<'a, 'tcx> HierarchicalAnalyzer<'a, 'tcx> {
    pub fn build_scc_hierarchy(&mut self) {
        let all_nodes: Vec<usize> = (0..self.graph.blocks.len()).collect();
        let preds = self.build_predecessors();
        self.scc_tree = self.decompose_subgraph(&all_nodes, &preds, &FxHashSet::default());

        self.flatten_scc_tree();
    }

    fn flatten_scc_tree(&mut self) {
        let mut queue = self.scc_tree.clone();
        while let Some(scc) = queue.pop() {
            if !scc.sub_sccs.is_empty() {
                queue.extend(scc.sub_sccs.clone());
            }
            self.dom_to_scc.insert(scc.dominator, scc);
        }
    }

    fn decompose_subgraph(
        &self,
        nodes: &[usize],
        preds: &FxHashMap<usize, Vec<usize>>,
        ignored_edges: &FxHashSet<(usize, usize)>,
    ) -> Vec<SccMetadata> {
        let mut result = Vec::new();
        let components = self.run_tarjan_on_subgraph(nodes, ignored_edges);

        for comp_nodes in components {
            if comp_nodes.len() == 1 {
                let u = comp_nodes[0];
                let has_self_loop =
                    self.graph.blocks[u].next.contains(&u) && !ignored_edges.contains(&(u, u));
                if !has_self_loop {
                    continue;
                }
            }

            let header = self.identify_header(&comp_nodes, nodes, preds, ignored_edges);
            let mut back_edges = Vec::new();
            for &u in &comp_nodes {
                if self.graph.blocks[u].next.contains(&header) {
                    if !ignored_edges.contains(&(u, header)) {
                        back_edges.push(u);
                    }
                }
            }

            let mut exits = Vec::new();
            let comp_set: FxHashSet<usize> = comp_nodes.iter().cloned().collect();
            for &u in &comp_nodes {
                for &target in &self.graph.blocks[u].next {
                    if !comp_set.contains(&target) {
                        exits.push(target);
                    }
                }
            }

            let mut next_level_ignored = ignored_edges.clone();
            for &source in &back_edges {
                next_level_ignored.insert((source, header));
            }

            let sub_sccs = self.decompose_subgraph(&comp_nodes, preds, &next_level_ignored);

            let scc_meta = SccMetadata {
                id: header,
                dominator: header,
                exits,
                back_edges,
                nodes: comp_nodes,
                sub_sccs,
            };
            result.push(scc_meta);
        }
        result
    }

    fn run_tarjan_on_subgraph(
        &self,
        nodes: &[usize],
        ignored_edges: &FxHashSet<(usize, usize)>,
    ) -> Vec<Vec<usize>> {
        let mut index = 0;
        let mut stack = Vec::new();
        let mut on_stack = FxHashSet::default();
        let mut indices = FxHashMap::default();
        let mut low_links = FxHashMap::default();
        let mut sccs = Vec::new();
        let node_set: FxHashSet<usize> = nodes.iter().cloned().collect();

        for &node in nodes {
            if !indices.contains_key(&node) {
                self.strongconnect(
                    node,
                    &node_set,
                    ignored_edges,
                    &mut index,
                    &mut stack,
                    &mut on_stack,
                    &mut indices,
                    &mut low_links,
                    &mut sccs,
                );
            }
        }
        sccs
    }

    fn strongconnect(
        &self,
        v: usize,
        node_set: &FxHashSet<usize>,
        ignored_edges: &FxHashSet<(usize, usize)>,
        index: &mut usize,
        stack: &mut Vec<usize>,
        on_stack: &mut FxHashSet<usize>,
        indices: &mut FxHashMap<usize, usize>,
        low_links: &mut FxHashMap<usize, usize>,
        sccs: &mut Vec<Vec<usize>>,
    ) {
        indices.insert(v, *index);
        low_links.insert(v, *index);
        *index += 1;
        stack.push(v);
        on_stack.insert(v);

        if let Some(block) = self.graph.blocks.get(v) {
            for &w in &block.next {
                if !node_set.contains(&w) || ignored_edges.contains(&(v, w)) {
                    continue;
                }
                if !indices.contains_key(&w) {
                    self.strongconnect(
                        w,
                        node_set,
                        ignored_edges,
                        index,
                        stack,
                        on_stack,
                        indices,
                        low_links,
                        sccs,
                    );
                    let low_v = low_links[&v];
                    let low_w = low_links[&w];
                    low_links.insert(v, std::cmp::min(low_v, low_w));
                } else if on_stack.contains(&w) {
                    let low_v = low_links[&v];
                    let index_w = indices[&w];
                    low_links.insert(v, std::cmp::min(low_v, index_w));
                }
            }
        }

        if low_links[&v] == indices[&v] {
            let mut component = Vec::new();
            loop {
                let w = stack.pop().unwrap();
                on_stack.remove(&w);
                component.push(w);
                if w == v {
                    break;
                }
            }
            sccs.push(component);
        }
    }

    fn identify_header(
        &self,
        comp_nodes: &[usize],
        scope_nodes: &[usize],
        preds: &FxHashMap<usize, Vec<usize>>,
        ignored_edges: &FxHashSet<(usize, usize)>,
    ) -> usize {
        let comp_set: FxHashSet<usize> = comp_nodes.iter().cloned().collect();
        for &node in comp_nodes {
            if let Some(predecessors) = preds.get(&node) {
                for &p in predecessors {
                    if ignored_edges.contains(&(p, node)) {
                        continue;
                    }
                    if !comp_set.contains(&p) {
                        return node;
                    }
                }
            } else if node == 0 {
                return 0;
            }
        }
        *comp_nodes.iter().min().unwrap()
    }

    fn build_predecessors(&self) -> FxHashMap<usize, Vec<usize>> {
        let mut preds = FxHashMap::default();
        for block in &self.graph.blocks {
            for &target in &block.next {
                preds
                    .entry(target)
                    .or_insert_with(Vec::new)
                    .push(block.index);
            }
        }
        preds
    }
}

impl<'a, 'tcx> HierarchicalAnalyzer<'a, 'tcx> {
    pub fn find_loop_slices(&self, scc: &SccMetadata) -> Vec<Slice> {
        let mut slices = Vec::new();
        let mut current_path = Vec::new();
        let mut visited = FxHashSet::default();
        let back_edge_sources: FxHashSet<usize> = scc.back_edges.iter().cloned().collect();
        let scc_nodes: FxHashSet<usize> = scc.nodes.iter().cloned().collect();

        self.dfs_slices(
            scc.dominator,
            &scc_nodes,
            &back_edge_sources,
            &FxHashSet::default(),
            &mut current_path,
            &mut visited,
            &mut slices,
            false,
        );
        slices
    }

    pub fn find_exit_slices(&self, scc: &SccMetadata) -> Vec<Slice> {
        let mut slices = Vec::new();
        let mut current_path = Vec::new();
        let mut visited = FxHashSet::default();
        let scc_nodes: FxHashSet<usize> = scc.nodes.iter().cloned().collect();
        let exit_targets: FxHashSet<usize> = scc.exits.iter().cloned().collect();

        self.dfs_slices(
            scc.dominator,
            &scc_nodes,
            &FxHashSet::default(),
            &exit_targets,
            &mut current_path,
            &mut visited,
            &mut slices,
            true,
        );
        slices
    }

    fn dfs_slices(
        &self,
        u: usize,
        scope_nodes: &FxHashSet<usize>,
        targets: &FxHashSet<usize>,
        exit_targets: &FxHashSet<usize>,
        path: &mut Vec<usize>,
        visited: &mut FxHashSet<usize>,
        results: &mut Vec<Slice>,
        is_exit_search: bool,
    ) {
        visited.insert(u);
        path.push(u);

        if is_exit_search {
            if let Some(block) = self.graph.blocks.get(u) {
                for &v in &block.next {
                    if exit_targets.contains(&v) {
                        results.push(Slice {
                            start_node: path[0],
                            end_node: v,
                            blocks: path.clone(),
                            is_exit: true,
                        });
                    }
                }
            }
        } else {
            if targets.contains(&u) {
                results.push(Slice {
                    start_node: path[0],
                    end_node: u,
                    blocks: path.clone(),
                    is_exit: false,
                });
            }
        }

        if scope_nodes.contains(&u) {
            if let Some(block) = self.graph.blocks.get(u) {
                for &v in &block.next {
                    if !visited.contains(&v) {
                        if scope_nodes.contains(&v) {
                            self.dfs_slices(
                                v,
                                scope_nodes,
                                targets,
                                exit_targets,
                                path,
                                visited,
                                results,
                                is_exit_search,
                            );
                        }
                    }
                }
            }
        }
        path.pop();
        visited.remove(&u);
    }
}

impl<'a, 'tcx> HierarchicalAnalyzer<'a, 'tcx> {
    pub fn simulate_slice(
        &mut self,
        start_state: &AbstractState,
        slice: &Slice,
    ) -> Vec<AbstractState> {
        // Changed return type to Vec
        let start_time = Instant::now();
        let start_alias = self.time_alias;
        let start_cons = self.time_constraint;
        let start_synth = self.time_path_synth;

        let mut active_states = vec![(start_state.clone(), 0)]; // (state, current_block_index_in_slice)
        let mut final_states = Vec::new();
        let blocks = &slice.blocks;

        while let Some((state, mut i)) = active_states.pop() {
            let t_alias_1 = Instant::now();
            state.restore_to(self.graph);
            self.time_alias += t_alias_1.elapsed();
            let mut current_path = state.path.clone();
            let mut aborted = false;

            while i < blocks.len() {
                let bb_idx = blocks[i];

                // --- Nested SCC Handling ---
                if i > 0 && self.dom_to_scc.contains_key(&bb_idx) {
                    let inner_scc = self.dom_to_scc.get(&bb_idx).unwrap().clone();

                    let mut current_inner_state = AbstractState::snapshot(self.graph);
                    current_inner_state.path = current_path.clone();

                    // Get all possible exits from the inner SCC
                    let exit_results = self.enumerate_scc(&inner_scc, current_inner_state);

                    let mut found_match = false;

                    // Fork the analysis for each valid exit that matches the slice's path
                    for (target_node, target_state) in exit_results {
                        // Look ahead in the slice to see if this exit matches the path
                        if let Some(offset) = blocks[i + 1..].iter().position(|&x| x == target_node)
                        {
                            let next_pos = i + 1 + offset;
                            // Push a new branch to worklist: continue from next_pos with the new state
                            active_states.push((target_state, next_pos));
                            found_match = true;
                        } else if target_node == slice.end_node {
                            active_states.push((target_state, blocks.len()));
                            found_match = true;
                        }
                    }

                    if !found_match {
                        // No valid path through SCC matches this slice
                        aborted = true;
                    }
                    // Stop processing this linear path; alternatives have been pushed to active_states
                    aborted = true;
                    break;
                }

                let t_alias_2 = Instant::now();
                if let Some(block) = self.graph.blocks.get(bb_idx) {
                    for &local in &block.assigned_locals {
                        self.graph.constants.remove(&local);
                    }

                    if let crate::analysis::core::alias_analysis::default::block::Term::Call(
                        terminator,
                    ) = &block.terminator
                    {
                        if let rustc_middle::mir::TerminatorKind::Call { destination, .. } =
                            &terminator.kind
                        {
                            let dest_local = destination.local.as_usize();
                            self.graph.constants.remove(&dest_local);
                        }
                    }
                }
                self.graph.alias_bb(bb_idx);
                self.time_alias += t_alias_2.elapsed();

                current_path.push(bb_idx);

                // DCP Constraint Check
                if i + 1 < blocks.len() {
                    let next_bb_idx = blocks[i + 1];
                    if !self.apply_branch_constraint(bb_idx, next_bb_idx) {
                        aborted = true;
                        break;
                    }
                }

                i += 1;
            }

            if aborted {
                continue;
            }

            // Boundary Constraint Check (Last block -> Target)
            if let Some(&last_block) = blocks.last() {
                let target = if slice.is_exit {
                    slice.end_node
                } else {
                    slice.start_node
                };
                if !self.apply_branch_constraint(last_block, target) {
                    continue;
                }
            }

            let t_alias_3 = Instant::now();
            let mut final_state = AbstractState::snapshot(self.graph);
            final_state.path = current_path;

            final_state.iter_count = state.iter_count;
            self.time_alias += t_alias_3.elapsed();

            final_states.push(final_state);
        }

        let total_elapsed = start_time.elapsed();
        let delta_alias = self.time_alias - start_alias;
        let delta_cons = self.time_constraint - start_cons;
        let delta_synth_inner = self.time_path_synth - start_synth;

        let my_synth_time = total_elapsed
            .saturating_sub(delta_alias)
            .saturating_sub(delta_cons)
            .saturating_sub(delta_synth_inner);

        self.time_path_synth += my_synth_time;
        final_states
    }

    fn apply_branch_constraint(&mut self, source_bb: usize, target_bb: usize) -> bool {
        let t_start = Instant::now();
        let block = &self.graph.blocks[source_bb];

        match &block.terminator {
            crate::analysis::core::alias_analysis::default::block::Term::Switch(terminator) => {
                if let TerminatorKind::SwitchInt { discr, targets } = &terminator.kind {
                    let discr_local = match discr {
                        Operand::Copy(place) | Operand::Move(place) => Some(place.local.as_usize()),
                        Operand::Constant(_) => None,
                    };

                    if let Some(mut local_id) = discr_local {
                        let mut explicit_val = None;
                        for (val, target) in targets.iter() {
                            if target.as_usize() == target_bb {
                                explicit_val = Some(val as usize);
                                break;
                            }
                        }

                        if let Some((subject_local, subject_val)) =
                            self.find_binary_eq_origin(source_bb, local_id)
                        {
                            let switch_bool_val = if let Some(v) = explicit_val {
                                v
                            } else if targets.otherwise().as_usize() == target_bb {
                                let has_zero = targets.iter().any(|(v, _)| v == 0);
                                if has_zero { 1 } else { 0 }
                            } else {
                                self.time_constraint += t_start.elapsed();
                                return true;
                            };

                            let root_local = self.resolve_local_in_block(source_bb, subject_local);

                            if switch_bool_val == 1 {
                                if let Some(&current_val) = self.graph.constants.get(&root_local) {
                                    if current_val != subject_val {
                                        self.time_constraint += t_start.elapsed();
                                        return false;
                                    }
                                } else {
                                    self.graph.constants.insert(root_local, subject_val);
                                }
                            } else {
                                if let Some(&current_val) = self.graph.constants.get(&root_local) {
                                    if current_val == subject_val {
                                        self.time_constraint += t_start.elapsed();
                                        return false;
                                    }
                                }
                            }
                            self.time_constraint += t_start.elapsed();
                            return true;
                        }

                        if let Some(&origin) = self.graph.discriminants.get(&local_id) {
                            local_id = origin;
                        }
                        let root_local = self.resolve_local_in_block(source_bb, local_id);

                        if let Some(current_val) = self.get_constant_value(source_bb, root_local) {
                            if let Some(switch_val) = explicit_val {
                                if current_val != switch_val {
                                    self.time_constraint += t_start.elapsed();
                                    return false;
                                }
                            } else if targets.otherwise().as_usize() == target_bb {
                                for (val, _) in targets.iter() {
                                    if val as usize == current_val {
                                        self.time_constraint += t_start.elapsed();
                                        return false;
                                    }
                                }
                            }
                        } else {
                            if let Some(switch_val) = explicit_val {
                                self.graph.constants.insert(root_local, switch_val);
                            }
                        }
                    }
                }
            }
            _ => {}
        }
        self.time_constraint += t_start.elapsed();
        true
    }

    fn get_constant_value(&self, bb: usize, local: usize) -> Option<usize> {
        if let Some(&v) = self.graph.constants.get(&local) {
            return Some(v);
        }
        self.find_constant_assignment(bb, local)
    }

    fn find_constant_assignment(&self, bb: usize, local_id: usize) -> Option<usize> {
        use rustc_middle::mir::{Const, Operand, Rvalue, StatementKind};
        let body = self.graph.tcx.optimized_mir(self.graph.def_id);
        let block = &body.basic_blocks[rustc_middle::mir::BasicBlock::from_usize(bb)];
        let tcx = self.graph.tcx;

        let typing_env = rustc_middle::ty::TypingEnv::post_analysis(tcx, self.graph.def_id);

        for stmt in block.statements.iter().rev() {
            if let StatementKind::Assign(box (place, rvalue)) = &stmt.kind {
                if place.local.as_usize() == local_id {
                    if let Rvalue::Use(Operand::Constant(c)) = rvalue {
                        if let Some(bits) = c.const_.try_eval_bits(tcx, typing_env) {
                            return Some(bits as usize);
                        }

                        match c.const_ {
                            Const::Val(val, _) => {
                                if let Some(scalar) = val.try_to_scalar_int() {
                                    return Some(scalar.to_uint(scalar.size()) as usize);
                                }
                            }

                            _ => {}
                        }

                        if let Some(val) = c.const_.try_eval_target_usize(tcx, typing_env) {
                            return Some(val as usize);
                        }
                    }

                    return None;
                }
            }
        }
        None
    }

    fn find_binary_eq_origin(&self, bb: usize, local_id: usize) -> Option<(usize, usize)> {
        use rustc_middle::mir::{BinOp, Operand, Rvalue, StatementKind};

        let body = self.graph.tcx.optimized_mir(self.graph.def_id);
        let block = &body.basic_blocks[rustc_middle::mir::BasicBlock::from_usize(bb)];
        let tcx = self.graph.tcx;

        for stmt in block.statements.iter().rev() {
            if let StatementKind::Assign(box (place, rvalue)) = &stmt.kind {
                if place.local.as_usize() == local_id {
                    if let Rvalue::BinaryOp(BinOp::Eq, box (op1, op2)) = rvalue {
                        let (op_place, op_const) = match (op1, op2) {
                            (Operand::Copy(p) | Operand::Move(p), Operand::Constant(c)) => (p, c),
                            (Operand::Constant(c), Operand::Copy(p) | Operand::Move(p)) => (p, c),
                            _ => return None,
                        };

                        let typing_env =
                            rustc_middle::ty::TypingEnv::post_analysis(tcx, self.graph.def_id);
                        let val = if let Some(scalar) = op_const.const_.try_to_scalar_int() {
                            Some(scalar.to_uint(scalar.size()) as usize)
                        } else if let Some(v) = op_const.const_.try_eval_bits(tcx, typing_env) {
                            Some(v as usize)
                        } else {
                            None
                        };

                        if let Some(v) = val {
                            return Some((op_place.local.as_usize(), v));
                        }
                    }

                    return None;
                }
            }
        }
        None
    }

    fn resolve_local_in_block(&self, bb: usize, start_local: usize) -> usize {
        use rustc_middle::mir::{Operand, Rvalue, StatementKind};
        let body = self.graph.tcx.optimized_mir(self.graph.def_id);
        let block = &body.basic_blocks[rustc_middle::mir::BasicBlock::from_usize(bb)];

        let mut cur_local = start_local;

        for stmt in block.statements.iter().rev() {
            if let StatementKind::Assign(box (place, rvalue)) = &stmt.kind {
                if place.local.as_usize() == cur_local {
                    if let Rvalue::Use(Operand::Copy(p) | Operand::Move(p)) = rvalue {
                        cur_local = p.local.as_usize();
                    } else {
                        break;
                    }
                }
            }
        }
        cur_local
    }
}

impl<'a, 'tcx> HierarchicalAnalyzer<'a, 'tcx> {
    pub fn run_analysis(&mut self) -> FxHashMap<usize, Vec<AbstractState>> {
        let start_total = Instant::now();

        let t_decomp = Instant::now();
        self.build_scc_hierarchy();
        self.time_decomp += t_decomp.elapsed();

        let mut worklist: VecDeque<(usize, AbstractState)> = VecDeque::new();
        let mut block_results: FxHashMap<usize, Vec<AbstractState>> = FxHashMap::default();

        worklist.push_back((0, AbstractState::new()));

        while let Some((bb_idx, state)) = worklist.pop_front() {
            if self.is_covered(bb_idx, &state, &block_results) {
                continue;
            }

            let t_alias_rec = Instant::now();
            self.record_state(bb_idx, state.clone(), &mut block_results);
            self.time_alias += t_alias_rec.elapsed();

            if let Some(scc) = self.dom_to_scc.clone().get(&bb_idx) {
                let exit_states = self.enumerate_scc(scc, state);

                for (target_bb, exit_state) in exit_states {
                    worklist.push_back((target_bb, exit_state));
                }
            } else {
                let t_alias_calc = Instant::now();

                state.restore_to(self.graph);
                self.graph.alias_bb(bb_idx);

                let mut current_path = state.path.clone();
                if current_path.last() != Some(&bb_idx) {
                    current_path.push(bb_idx);
                }

                if self.graph.blocks[bb_idx].next.is_empty() {
                    self.graph.merge_results();
                }

                let mut new_state = AbstractState::snapshot(self.graph);
                new_state.path = current_path;

                self.time_alias += t_alias_calc.elapsed();

                if let Some(block) = self.graph.blocks.clone().get(bb_idx) {
                    for &succ in &block.next {
                        new_state.restore_to(self.graph);

                        if self.apply_branch_constraint(bb_idx, succ) {
                            let mut next_state = AbstractState::snapshot(self.graph);
                            next_state.path = new_state.path.clone();
                            worklist.push_back((succ, next_state));
                        }
                    }
                }
            }
        }

        self.time_total = start_total.elapsed();

        let time_other = self
            .time_total
            .saturating_sub(self.time_decomp)
            .saturating_sub(self.time_constraint)
            .saturating_sub(self.time_path_synth)
            .saturating_sub(self.time_alias);

        block_results
    }

    fn enumerate_scc(
        &mut self,
        scc: &SccMetadata,
        entry_state: AbstractState,
    ) -> Vec<(usize, AbstractState)> {
        let t_cache = Instant::now();
        for (id, cached_entry, cached_result) in &self.summary_cache {
            if *id == scc.id {
                if self.is_substate_of(&entry_state, cached_entry)
                    && self.is_substate_of(cached_entry, &entry_state)
                {
                    self.time_alias += t_cache.elapsed();
                    return cached_result.clone();
                }
            }
        }

        let t_synth = Instant::now();
        let loop_slices = self.find_loop_slices(scc);
        let exit_slices = self.find_exit_slices(scc);
        self.time_path_synth += t_synth.elapsed();

        let mut worklist = VecDeque::new();
        worklist.push_back(entry_state.clone());
        let mut history: Vec<AbstractState> = Vec::new();
        let mut final_exits = Vec::new();

        let mut splicing_count = 0;
        while let Some(current_state) = worklist.pop_front() {
            if !self.is_fresh(&current_state, &history) {
                continue;
            }
            splicing_count += 1;

            history.retain(|old_state| !self.is_substate_of(old_state, &current_state));
            history.push(current_state.clone());

            for slice in &loop_slices {
                let next_states = self.simulate_slice(&current_state, slice);
                for mut next_state in next_states {
                    next_state.iter_count += 1;
                    if next_state.iter_count > 1 {
                        rap_debug!(
                            "Path Iteration Depth: {} | Path: {:?}",
                            next_state.iter_count,
                            next_state.path
                        );
                    }
                    worklist.push_back(next_state);
                }
            }

            for slice in &exit_slices {
                let out_states = self.simulate_slice(&current_state, slice);
                for out_state in out_states {
                    final_exits.push((slice.end_node, out_state));
                }
            }
        }

        let t_dedup = Instant::now();
        let mut unique_exits: Vec<(usize, AbstractState)> = Vec::new();
        for (target, state) in final_exits.clone() {
            let mut is_redundant = false;
            for (u_target, u_state) in &unique_exits {
                if target == *u_target && self.is_substate_of(&state, u_state) {
                    is_redundant = true;
                    break;
                }
            }
            if !is_redundant {
                unique_exits.retain(|(t, s)| *t != target || !self.is_substate_of(s, &state));
                unique_exits.push((target, state));
            }
        }
        self.time_alias += t_dedup.elapsed();

        self.summary_cache
            .push((scc.id, entry_state, unique_exits.clone()));
        unique_exits
    }

    fn is_fresh(&self, new_state: &AbstractState, history: &[AbstractState]) -> bool {
        for old_state in history {
            if self.is_substate_of(new_state, old_state) {
                return false;
            }
        }
        true
    }

    /// Check if state `a` is covered by `b` (A <= B).
    /// Returns true ONLY if:
    /// 1. A's alias relations are a subset of B's.
    /// 2. A's path constraints are compatible with B's (A must strictly agree with B).
    fn is_substate_of(&self, a: &AbstractState, b: &AbstractState) -> bool {
        if a.constants.len() < b.constants.len() {
            return false;
        }

        for (var, val_b) in &b.constants {
            match a.constants.get(var) {
                Some(val_a) => {
                    if val_a != val_b {
                        return false; // Conflict: choice=First vs choice=Second
                    }
                }
                None => {
                    // If 'a' lacks a constraint that 'b' has, 'a' is actually "more general"
                    // (or from a different path merge), so it's not a substate.
                    return false;
                }
            }
        }

        for set_a in &a.alias_sets {
            // Skip empty/singleton sets as they carry no alias info
            if set_a.len() <= 1 {
                continue;
            }

            let mut found_container = false;
            for set_b in &b.alias_sets {
                if set_a.is_subset(set_b) {
                    found_container = true;
                    break;
                }
            }

            // If we found an alias relation in A that isn't covered by B, A is new info.
            if !found_container {
                return false;
            }
        }

        true
    }

    fn is_covered(
        &self,
        bb: usize,
        state: &AbstractState,
        results: &FxHashMap<usize, Vec<AbstractState>>,
    ) -> bool {
        if let Some(history) = results.get(&bb) {
            return !self.is_fresh(state, history);
        }
        false
    }

    fn record_state(
        &self,
        bb: usize,
        state: AbstractState,
        results: &mut FxHashMap<usize, Vec<AbstractState>>,
    ) {
        results.entry(bb).or_insert_with(Vec::new).push(state);
    }
}
