#[derive(PartialEq, Clone, Copy)]
pub enum LoopState {
    Start,
    Processing,
    Finishing,
    Done,
}

enum State_test {
    Load,
    Process,
    Finish,
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum State_2 {
    Init,
    Process,
    Final,
}

#[derive(PartialEq, Clone, Copy)]
pub enum BranchMode {
    PathA,
    PathB,
    PathC,
    DeadPath,
}

fn random_test() -> bool {
    use std::time::{SystemTime, UNIX_EPOCH};
    let start = SystemTime::now();
    let since_the_epoch = start
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards");
    since_the_epoch.subsec_nanos() % 2 == 0
}

enum Selector {
    First,
    Second,
}
struct Node {
    data: i32,
}

/// Expected alias analysis result: (0, 2), (0, 3)
pub fn case_1<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, start_state: LoopState) -> &'a i32 {
    let mut res = p3;
    let mut state = start_state;
    let mut outer_iter = 0;

    loop {
        // Outer loop logic
        if state == LoopState::Start {
            res = p1;

            // Time Trap: We only advance state after a "warmup" iteration
            if outer_iter > 0 {
                state = LoopState::Processing;
            }

            loop {
                // Inner loop: Correlated to state being Processing
                if state == LoopState::Processing {
                    res = p2;
                    state = LoopState::Finishing;
                }

                // Deterministic break based on state
                if state == LoopState::Finishing {
                    break;
                }

                // Escape valve for the warmup phase
                if outer_iter == 0 {
                    break;
                }
            }
        }

        if state == LoopState::Finishing || state == LoopState::Done {
            break;
        }

        outer_iter += 1;
        if outer_iter > 3 {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1),  (0, 3), (1, 3)
pub fn case_2<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, enable_mutation: bool) -> &'a i32 {
    let mut res = p2;
    let mut steps = 0;

    loop {
        res = *p1;
        steps += 1;

        let mut inner_count = 0;
        loop {
            // Time Trap: Mutation only happens on inner_count == 1 (The second pass)
            // AND the Phase 2 constraint (enable_mutation) must hold.
            if enable_mutation && inner_count == 1 {
                *p1 = p3;
                res = p3;
            }

            if inner_count >= 2 {
                break;
            }
            inner_count += 1;
        }
        if steps >= 3 {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_3<'a>(
    p1: &'a i32,
    p2: &'a i32,
    p3: &'a i32,
    _p4: &'a i32,
    mode: BranchMode,
) -> &'a i32 {
    let mut res = p1;
    let mut time = 0;

    loop {
        // Outer
        loop {
            // Middle
            loop {
                if let BranchMode::DeadPath = mode {
                    if time > 2 {
                        res = p2;
                    }
                }
                if time > 0 {
                    break;
                }
                time += 1;
            }

            if let BranchMode::PathA = mode {
                // Delayed alias: Only after inner loop has run at least once
                if time > 1 {
                    res = p3;
                }
            }
            if time > 2 {
                break;
            }
            time += 1;
        }
        if time > 4 {
            break;
        }
        time += 1;
    }
    res
}

/// Expected alias analysis result:(0, 2)
pub fn case_4<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, mut guard: bool) -> &'a i32 {
    let mut res = p1;
    let mut i = 0;
    let mut history_toggle = false;

    loop {
        if guard ^ history_toggle {
            let mut inner_ptr = p3;
            loop {
                inner_ptr = p2;
                if i >= 1 {
                    break;
                }
                i += 1;
            }
            res = inner_ptr;
        }

        history_toggle = !history_toggle;

        if i >= 2 {
            break;
        }
        i += 1;
    }
    res
}

/// Expected alias analysis result:(0, 2),  (0, 4)
pub fn case_5<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, iter_max: i32) -> &'a i32 {
    let mut res = p1;
    let mut outer_i = 0;

    loop {
        let mut temp = res;
        let mut inner_i = 0;

        loop {
            // Time Trap: Depends on accumulated `outer_i` from history.
            if (outer_i + inner_i) > 2 {
                temp = p2;
            } else {
                temp = p3;
            }
            if inner_i >= 1 {
                break;
            }
            inner_i += 1;
        }
        res = temp;

        // Late Binding: p4 is only assigned at the very end of a long chain.
        if outer_i == iter_max && outer_i > 5 {
            res = p4;
        }

        if outer_i >= 4 {
            break;
        } // Fixed iteration depth
        outer_i += 1;
    }
    res
}

/// Expected alias analysis result: (0, 3), (0, 5), (1, 3)
pub fn case_6<'a>(
    p1: &mut &'a i32,
    p2: &'a i32,
    p3: &'a i32,
    p4: &'a i32,
    p5: &'a i32,
    swap_mode: bool,
) -> &'a i32 {
    let mut res = p4;
    let mut i = 0;
    let mut has_swapped = false;

    loop {
        // Time Trap: If we swapped once, we keep swapping regardless of mode.
        if swap_mode || has_swapped {
            loop {
                if i % 2 == 0 {
                    *p1 = p2;
                } else {
                    *p1 = p3;
                }
                has_swapped = true; // Set the latch
                if i > 0 {
                    break;
                }
                i += 1;
            }
            res = *p1;
        } else {
            res = p5;
        }
        if i >= 3 {
            break;
        }
        i += 1;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_7<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, limit: i32) -> &'a i32 {
    let mut res = p1;
    let mut counter = 0;

    'outer: loop {
        loop {
            // Time Trap: We rely on the counter incrementing across inner/outer loops
            if counter == limit + 2 {
                res = p2;
                break 'outer;
            }
            if counter > limit + 5 {
                res = p3; // Only reachable if we spin a long time
                break;
            }
            counter += 1;
            if counter > 10 {
                break 'outer;
            }
        }
        // Implicit continue of outer
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2)
pub fn case_8<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, mut flag: bool) -> &'a i32 {
    let mut res = p3;
    let mut count = 0;

    loop {
        if flag {
            res = p1;
        }

        loop {
            if !flag {
                res = p2;
            }
            break;
        }

        flag = !flag; // Mutation of control flow variable

        if count >= 1 {
            break;
        }
        count += 1;
    }
    res
}

/// Expected alias analysis result: (0, 3), (1, 3)
pub fn case_9<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p2;
    let mut i = 0;
    loop {
        let mut j = 0;
        loop {
            let mut k = 0;
            loop {
                // Temporal Mutation: Deepest update.
                // Requires exact alignment of i, j, k which represent temporal depth.
                if i == 1 && j == 1 && k == 1 {
                    *p1 = p3;
                    res = *p1;
                }
                if k >= 1 {
                    break;
                }
                k += 1;
            }
            if j >= 1 {
                break;
            }
            j += 1;
        }
        if i >= 1 {
            break;
        }
        i += 1;
    }
    res
}

/// Expected alias analysis result: (0, 2), (0, 3)
pub fn case_10<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, mut mode: BranchMode) -> &'a i32 {
    let mut res = p3;
    let mut tries = 0;
    loop {
        if let BranchMode::PathA = mode {
            // Time Trap: If PathA, we switch to PathB for the next iteration instead of returning immediately
            if tries == 0 {
                mode = BranchMode::PathB;
                tries += 1;
                continue;
            }
            return p1;
        }
        if let BranchMode::PathB = mode {
            res = p2;
            break;
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_11<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, iterations: i32) -> &'a i32 {
    let mut res = p1;
    let mut i = 0;
    let mut latch = false; // "Termination-Dependent State"

    loop {
        if i < iterations {
            res = p2;
            latch = true; // We visited the p2 assignment
            i += 1;
            continue;
        }

        // Time Trap: If we exit here, we verify if latch was set.
        if i >= iterations {
            if latch {
                // If we looped at least once, we might return p2 (current res) or p3.
                // Here we assign p3.
                res = p3;
            }
            break;
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4)
pub fn case_12<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, mut x: i32) -> &'a i32 {
    loop {
        // Temporal Mutation: x changes every iteration.
        if x == 1 {
            return p1;
        }
        if x > 5 {
            if x > 10 {
                return p2;
            }
            x -= 1; // Time Trap: Converges towards 5.
            continue;
        }
        if x == 5 {
            return p4;
        } // Reachable after decay

        break;
    }
    p3
}

/// Expected alias analysis result:(0, 2), (0, 3), (1, 2)
pub fn case_13<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, do_alias: bool) -> &'a i32 {
    let mut warmup = true;
    loop {
        if warmup {
            warmup = false;
            // Time Trap: First iteration effectively a no-op regarding exit/alias, forcing a loop.
            continue;
        }

        if do_alias {
            *p1 = p2;
            return *p1;
        }
        return p3;
    }
}

/// Expected alias analysis result:(0, 2)
pub fn case_14<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p1;
    let mut dynamic_val = 0;
    loop {
        // Time Trap: The condition `dynamic_val == 2` becomes true over time.
        if dynamic_val == 2 {
            res = p2;
            break;
        }

        if dynamic_val == 10 {
            // Still effectively unreachable in this short loop setup
            return p3;
        }

        dynamic_val += 1;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4)
pub fn case_15<'a>(
    p1: &'a i32,
    p2: &'a i32,
    p3: &'a i32,
    p4: &'a i32,
    start_selector: i32,
) -> &'a i32 {
    let mut res = p1;
    let mut selector = start_selector;

    loop {
        // Time Trap: If we don't hit a case, we increment selector and try again.
        if selector == 1 {
            res = p2;
            break;
        }
        if selector == 2 {
            res = p3;
            break;
        }
        if selector == 3 {
            res = p4;
            break;
        }

        if selector > 3 {
            break;
        }
        selector += 1; // Mutation
    }
    res
}

/// Expected alias analysis result:(0, 1)
pub fn case_16<'a>(p1: &'a i32, _p2: &'a i32, p3: &'a i32, mut condition: bool) -> &'a i32 {
    loop {
        if condition {
            return p1;
        } else {
            condition = true; // Enable the other path next time
                              // continue implicitly
        }
    }
}

/// Expected alias analysis result:(0, 2)
pub fn case_17<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, loop_count: i32) -> &'a i32 {
    let mut res = p1;
    let mut i = 0;
    loop {
        res = p2;
        if i >= loop_count {
            break;
        }

        res = p3;

        i += 1;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_18<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, mode: BranchMode) -> &'a i32 {
    let mut res = p1;
    let mut prev_res = p1; // History

    loop {
        match mode {
            BranchMode::PathA => {
                res = p2;
                prev_res = p2; // Save history
                               // Loop back
            }
            BranchMode::PathB => {
                // Time Trap: Return the *previous* result, not current.
                return prev_res;
            }
            _ => {
                return p3;
            }
        }
        // If PathA, we break to avoid infinite loop for benchmark
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 3)
pub fn case_19<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, input_flag: bool) -> &'a i32 {
    let mut res = p1;
    let mut shared_counter = 0;

    // Sibling A
    loop {
        if input_flag {
            res = p2;
            shared_counter = 5; // Set state
        }
        break;
    }

    // Sibling B
    loop {
        // Time Trap: Only alias p3 if Sibling A set the counter
        if shared_counter > 0 {
            res = p3;
            shared_counter -= 1;
        }
        break;
    }
    res
}

/// Expected alias analysis result: (0, 2), (0, 3), (1, 2)
pub fn case_20<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, do_write: bool) -> &'a i32 {
    // Sibling A
    loop {
        if do_write {
            *p1 = p2;
        }
        break;
    }

    let mut res = p3;
    let mut cycles = 0;
    // Sibling B
    loop {
        // Time Trap: We read *p1 only after a local cycle
        if cycles > 0 {
            if do_write {
                res = *p1;
            }
        }
        if cycles >= 1 {
            break;
        }
        cycles += 1;
    }
    res
}

/// Expected alias analysis result:(0, 1),(0, 4)
pub fn case_21<'a>(
    p1: &'a i32,
    p2: &'a i32,
    p3: &'a i32,
    p4: &'a i32,
    mut sequence: i32,
) -> &'a i32 {
    let mut res = p1;
    // Loop 1
    loop {
        if sequence == 0 {
            res = p2;
            sequence += 1;
        }
        break;
    }
    // Loop 2
    loop {
        if sequence == 1 {
            res = p3;
            sequence += 1;
        }
        break;
    }
    // Loop 3
    loop {
        if sequence == 2 {
            res = p4;
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_22<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, run_b: bool) -> &'a i32 {
    let mut res = p1;
    let mut loop_a_ran = false;
    // Loop A
    loop {
        res = p2;
        loop_a_ran = true;
        break;
    }

    if run_b {
        // Loop B
        loop {
            // Time Trap: Only assign p3 if A ran (which it always does here, but logic is explicit)
            if loop_a_ran {
                res = p3;
            }
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_23<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, use_temp1: bool) -> &'a i32 {
    let mut temp1 = p1;
    let mut a_iters = 0;
    // Loop A
    loop {
        temp1 = p2;
        a_iters += 1;
        if a_iters >= 2 {
            break;
        } // Runs twice
    }

    let temp2 = p3;
    // Loop B
    loop {
        break;
    }

    // Time Trap: Merge depends on iteration count
    if a_iters == 2 && use_temp1 {
        temp1
    } else {
        temp2
    }
}

/// Expected alias analysis result:(0, 1), (0, 3), (0, 4)
pub fn case_24<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, mode: i32) -> &'a i32 {
    let mut res = p1;
    let mut history = 0;
    // Loop A
    loop {
        if mode == 1 {
            res = p2;
            history = 1;
        }
        break;
    }
    // Loop B
    loop {
        // Time Trap: Correlated to A's execution
        if history == 1 {
            // If we came from A, we might overwrite with p3
            res = p3;
        } else if mode == 3 {
            res = p4;
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)
pub fn case_25<'a>(
    p1: &'a i32,
    p2: &'a i32,
    p3: &'a i32,
    p4: &'a i32,
    p5: &'a i32,
    start_mode: i32,
) -> &'a i32 {
    let mut res = p1;
    let mut mode = start_mode;
    let mut i = 0;
    loop {
        // Time Trap: Mode increments.
        match mode {
            2 => res = p2,
            3 => res = p3,
            4 => res = p4,
            5 => res = p5,
            _ => (),
        }

        mode += 1; // Rotation

        if i >= 1 {
            break;
        } // Runs twice, so covers at least 2 modes
        i += 1;
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3), (0, 4), (1, 3)
pub fn case_26<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, path: i32) -> &'a i32 {
    let mut res = p4;
    let mut visits = 0;
    loop {
        if path == 1 {
            res = p2;
        } else if path == 2 {
            // Time Trap: Only mutate if we've visited this loop before (visits > 0)
            if visits > 0 {
                *p1 = p3;
                res = *p1;
            }
        } else {
            res = p4;
        }

        if visits >= 1 {
            break;
        }
        visits += 1;
    }
    res
}

/// Expected alias analysis result: (0, 2), (0, 3), (0, 4)
pub fn case_27<'a>(
    p1: &'a i32,
    p2: &'a i32,
    p3: &'a i32,
    p4: &'a i32,
    mut x: bool,
    y: bool,
) -> &'a i32 {
    let mut res = p1;
    let mut i = 0;
    loop {
        // Time Trap: x toggles
        if x {
            if y {
                res = p2;
            } else {
                res = p3;
            }
        } else {
            if y {
                res = p4;
            }
        }

        x = !x; // Toggle

        if i >= 1 {
            break;
        }
        i += 1;
    }
    res
}

/// Expected alias analysis result:(0, 3)
pub fn case_28<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, start_idx: i32) -> &'a i32 {
    let mut res = p1;
    let mut idx = start_idx;
    loop {
        // Time Trap: idx increments, eventually hitting the 'else' case
        if idx == 0 {
            res = p2;
        } else if idx == 1 {
            res = p2;
        } else if idx == 2 {
            res = p2;
        } else {
            res = p3;
        }

        idx += 1;
        if idx > 3 {
            break;
        }
    }

    res
}

/// Expected alias analysis result:(0, 3), (0, 4)
pub fn case_29<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, mut val: i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if val < 0 {
            res = p2;
            val = 1; // Jump to > 0 state next
            continue;
        } else if val == 0 {
            return p3;
        } else if val > 0 {
            res = p4;
            break;
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3), (1, 3)
pub fn case_30<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, mut mode: BranchMode) -> &'a i32 {
    let mut res = p2;
    let mut i = 0;
    loop {
        match mode {
            BranchMode::PathA => {
                res = *p1;
                mode = BranchMode::PathB; // Cycle
            }
            BranchMode::PathB => {
                *p1 = p3;
                res = p2;
                mode = BranchMode::PathC; // Cycle
            }
            BranchMode::PathC => {
                res = p3;
            }
            _ => (),
        }

        if i >= 2 {
            break;
        } // Allow 3 steps
        i += 1;
    }
    res
}

/// Expected alias analysis result: (0,2)
fn case_31<'a>(x: &'a i32, y: &'a i32) -> &'a i32 {
    let mut p = x;
    let mut state = State_test::Load;

    loop {
        match state {
            State_test::Load => {
                p = x;
                state = State_test::Process;
            }
            State_test::Process => {
                p = y;
                state = State_test::Finish;
            }
            State_test::Finish => {
                break;
            }
        }
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case_32<'a>(x: &'a Node, y: &'a Node, z: &'a Node) -> &'a Node {
    let mut current = x;
    let mut next = y;

    loop {
        current = next;
        next = z;

        if true {
            break;
        }
    }
    current
}

/// Expected alias analysis result: (0,1)
fn case_33<'a>(x: &'a i32, y: &'a i32, z: &'a i32) -> &'a i32 {
    let mut stage1 = x;
    let mut stage2 = y; // initial noise
    let mut r = z; // initial noise

    for _ in 0..3 {
        r = stage2; // Iter 1: r<-y; Iter 2: r<-x; ...
        stage2 = stage1; // Iter 1: y<-x; ...
    }
    r
}

/// Expected alias analysis result: (0,1),(0,3)
fn case_34<'a>(x: &'a i32, y: &'a i32, z: &'a i32, choice: Selector) -> &'a i32 {
    let mut r = x;
    let mut q = z;

    // [Outer SCC]: Configuration Phase
    loop {
        // Defines the 'Source' of the pipeline based on 'choice'
        // This is the "Input Valve"
        let mut p = match choice {
            Selector::First => y,  // Path A: Source is 'y' (Polluted/Distractor)
            Selector::Second => x, // Path B: Source is 'x' (Clean/Target)
        };

        // [Inner SCC]: Propagation Phase (The Pipeline)
        loop {
            if random_test() {
                break;
            }
            r = match choice {
                Selector::First => x,
                Selector::Second => p,
            };
            p = z;
        }
        if random_test() {
            break;
        }
    }
    r
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_35<'a>(x: &'a i32, y: &'a i32) -> &'a i32 {
    let mut stage3 = x;
    let mut stage2 = x;
    let mut stage1 = y; // Source of new data

    loop {
        stage3 = stage2; // Iter 1: x, Iter 2: x, Iter 3: y
        stage2 = stage1; // Iter 1: y, Iter 2: y
                         // stage1 is constant y

        if random_test() {
            break;
        }
    }
    stage3
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
pub fn case_36<'a>(x: &'a i32, y: &'a i32, z: &'a i32) -> &'a i32 {
    let mut p = x;
    loop {
        if random_test() {
            return p;
        } // Returns current (x on iter 1, z on iter 2)

        p = z; // Update for next iteration

        if random_test() {
            return y;
        } // Returns explicit y
    }
}

/// Expected alias analysis result: (0,1),(0,2),(0,3),(0,4)
fn case_37<'a>(a: &'a i32, b: &'a i32, c: &'a i32, d: &'a i32) -> &'a i32 {
    let mut p = a; // Iter 1: p -> a
    let mut next_1 = b;
    let mut next_2 = c;

    loop {
        if random_test() {
            break;
        } // Exit could happen at any stage

        // Pipeline shift
        let temp = p;
        p = next_1; // Iter 2: p -> b, Iter 3: p -> c
        next_1 = next_2; // Prep for next
        next_2 = d; // Iter 4: p -> d
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_38<'a>(x: &'a i32, y: &'a i32, z: &'a i32) -> &'a i32 {
    let mut r = z;
    loop {
        // Level 1
        let mut l1 = x;
        loop {
            // Level 2
            let mut l2 = y;
            loop {
                // Level 3
                if random_test() {
                    r = l1; // r -> x
                    break;
                }
                if random_test() {
                    r = l2; // r -> y
                    break;
                }
                // Loop carried in Level 3
                l2 = z;
                if random_test() {
                    break;
                }
            }
            if random_test() {
                break;
            }
            // Loop carried in Level 2
            l1 = z;
        }
        if random_test() {
            break;
        }
    }
    r
}

/// Expected alias analysis result: (0,3)
fn case_39<'a>(a: &'a i32, b: &'a i32, c: &'a i32) -> &'a i32 {
    let mut state = State_2::Init;
    let mut r = a;

    loop {
        match state {
            State_2::Init => {
                r = a;
                state = State_2::Process;
            }
            State_2::Process => {
                r = b;
                state = State_2::Final;
            }
            State_2::Final => {
                r = c;
                if random_test() {
                    break;
                }
                state = State_2::Init; // Reset
            }
        }
    }
    r
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_40<'a>(a: &'a i32, b: &'a i32, c: &'a i32) -> &'a i32 {
    let mut level1 = a;
    let mut level2 = b;

    loop {
        let temp = level1;
        level1 = level2; // a -> b
        level2 = c; // b -> c

        if random_test() {
            return temp;
        } // Returns old level1

        if random_test() {
            break;
        }
    }
    level1
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_41<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut res = arg1;
    let mut state = 0;

    loop {
        // Obfuscation: intermediate pointer
        let mut temp = arg6;

        if state == 0 {
            temp = arg1;
        } else if state == 1 {
            // This path is only reachable after the loop loops once
            temp = arg2;
        } else {
            temp = arg3; // Dead code in practice if loop breaks early, but possible if random fails often
        }

        if random_test() {
            res = temp;

            if random_test() {
                break;
            }
        }

        // State transition
        if state == 0 {
            state = 1;
        } else if state == 1 {
            state = 2;
        }
    }
    res
}

/// Expected alias analysis result: (0,4)
fn case_42<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
    arg7: &'a i32,
) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;
    let mut count = 0;

    loop {
        // Capture previous state of q
        p = q;

        // Update q based on counter (State Machine)
        if count == 0 {
            q = arg3;
        } else if count == 1 {
            q = arg4;
        }

        // Escape condition
        if random_test() && count > 1 {
            return p;
        }

        count += 1;
        if count > 5 {
            break;
        }
    }

    p
}

/// Expected alias analysis result: (0,3)
fn case_43<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut p1 = arg1;
    let mut p2 = arg2;
    let mut p3 = arg3;

    let mut steps = 0;
    loop {
        // Rotate pointers: p1 takes p2, p2 takes p3, p3 takes p1
        let temp = p1;
        p1 = p2;
        p2 = p3;
        p3 = temp;

        if steps == 1 {
            return p1;
        }
        steps += 1;
    }
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_44<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
    arg7: &'a i32,
) -> &'a i32 {
    let mut flag_a = false;
    let mut flag_b = false;
    let mut p = arg7;

    loop {
        if !flag_a && !flag_b {
            p = arg1;
            flag_a = true; // Next: True/False
        } else if flag_a && !flag_b {
            p = arg2;
            flag_b = true; // Next: True/True
        } else if flag_a && flag_b {
            p = arg3;
            // No update, stuck here
        } else {
            // False/True state - Unreachable logic unless flags mutated elsewhere
            p = arg4;
        }

        if random_test() {
            return p;
        }
    }
}

/// Expected alias analysis result: (0,5)
fn case_45<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
    arg7: &'a i32,
) -> &'a i32 {
    let mut x = arg1;
    let mut y = arg2;
    let mut z = arg3;
    let mut step = 0;

    loop {
        z = y; // z takes old y
        y = x; // y takes old x

        if step == 0 {
            x = arg4;
        }
        if step == 1 {
            x = arg5;
        }

        if random_test() && step > 2 {
            return z;
        }
        step += 1;
    }
}

/// Expected alias analysis result: (0,1),(0,2),(0,4)
fn case_46<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut p = arg1;
    let mut outer = 0;

    loop {
        let mut mid = 0;
        loop {
            let mut inner = 0;
            loop {
                if outer == 1 && mid == 1 {
                    p = arg4;
                } else if inner == 5 {
                    p = arg2;
                }

                if random_test() {
                    return p;
                }
                inner += 1;
                if inner > 5 {
                    break;
                }
            }
            mid += 1;
            if mid > 2 {
                break;
            }
        }
        outer += 1;
        // Outer logic: if outer becomes 1, arg4 is possible.
        // Initial: arg1. Inner loop: arg2.
        if outer > 2 {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_47<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
    arg7: &'a i32,
) -> &'a i32 {
    let mut p = arg1;
    let mut step = 0;

    loop {
        let mut left = p;
        let mut right = p;

        if step % 2 == 0 {
            left = arg2;
        } else {
            right = arg3;
        }

        // Merge
        if random_test() {
            p = left;
        } else {
            p = right;
        }

        if step > 3 {
            return p;
        }
        step += 1;
    }
}

/// Expected alias analysis result: (0,2),(0,3),(0,4),(0,5)
fn case_48<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut current = arg1;
    let mut next_val = arg2;
    let mut i = 0;

    loop {
        current = next_val;

        // Calc next_val for NEXT iteration
        if i == 0 {
            next_val = arg3;
        } else if i == 1 {
            next_val = arg4;
        } else {
            next_val = arg5;
        }

        if random_test() {
            return current;
        }
        i += 1;
    }
}

/// Expected alias analysis result: (0,1),(0,2),(0,3),(0,4)
fn case_49<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut p = arg1;
    let mut prev = arg6;
    let mut i = 0;

    loop {
        prev = p;

        if i == 0 {
            p = arg2;
        } else if i == 1 {
            p = arg3;
        } else {
            p = arg4;
        }

        if random_test() {
            return prev;
        }

        i += 1;
        if i > 10 {
            break;
        }
    }
    prev
}

/// Expected alias analysis result: (0,2),(0,3),(0,4),(0,5)
fn case_50<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
    arg7: &'a i32,
    arg8: &'a i32,
) -> &'a i32 {
    let mut p = arg1; // 1
    let mut q = arg2; // 2
    let mut state = 0;

    loop {
        // Delayed: p takes old q
        p = q;

        // State Machine for q
        if state == 0 {
            // Iter 1: q becomes 3. p was 2.
            q = arg3;
            state = 1;
        } else if state == 1 {
            // Iter 2: q becomes 4. p was 3.
            q = arg4;
            state = 2;
        } else {
            // Iter 3+: q becomes 5. p was 4.
            q = arg5;
        }

        // Distractor (False Path)
        if state > 100 {
            p = arg8;
        }

        // Correlated exit
        if random_test() {
            if state == 1 {
                // We are in Iter 1 end. p is arg2.
                return p;
            }
            if state == 2 {
                // We are in Iter 2 end. p is arg3.
                return p;
            }
            // Later: p is arg4, then arg5
            return p;
        }
    }
}

/// Expected alias analysis result: (0,1),(0,2)
fn case51<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut iter = 0;
    loop {
        // Delay alias generation
        if iter > 2 {
            if random_test() {
                p = arg2;
            }
        }

        if random_test() && iter > 5 {
            break;
        }
        iter += 1;
    }
    p
}

/// Expected alias analysis result: (0,1),(0,3)
fn case52<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut outer_warmup = 0;

    if random_test() {
        loop {
            // State dependency: only assign after warmup
            if outer_warmup > 0 {
                p = arg2;
            }

            if random_test() {
                // Late binding: arg3 appears last
                if outer_warmup > 2 {
                    p = arg3;
                    break;
                }
            }
            outer_warmup += 1;
        }
    }
    p
}

/// Expected alias analysis result: (0,3)
fn case53<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut flag = false;

    // SCC 1: Sets flag after iterations
    let mut i = 0;
    loop {
        if i > 2 {
            p = arg2;
            flag = true;
            break;
        }
        i += 1;
    }

    // SCC 2: Reads flag
    loop {
        if flag {
            // Only reachable if SCC 1 evolved enough
            if random_test() {
                p = arg3;
                break;
            }
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case54<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut outer_c = 0;
    loop {
        // Evolution: p changes only in later outer iterations
        if outer_c > 1 {
            p = arg2;
        }

        loop {
            // Inner loop logic acts as a delay
            if random_test() {
                break;
            }
        }

        if random_test() && outer_c > 3 {
            break;
        }
        outer_c += 1;
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case55<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut ticks = 0;
    loop {
        if ticks > 3 && random_test() {
            return arg2; // Late exit
        }
        p = arg3; // Immediate alias

        if random_test() {
            break;
        }
        ticks += 1;
    }
    p
}

/// Expected alias analysis result: (0,4)
fn case56<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut c1 = 0;
    loop {
        loop {
            p = arg2;
            let mut c3 = 0;
            loop {
                // Noise assignment to arg3 to confuse early analysis
                if random_test() {
                    p = arg3;
                }
                if c3 > 1 && random_test() {
                    break;
                }
                c3 += 1;
            }
            // Target assignment arg4
            if c1 > 2 && random_test() {
                p = arg4;
                break;
            }
        }
        if random_test() {
            break;
        }
        c1 += 1;
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case57<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut step = 0;
    loop {
        if random_test() {
            p = arg2;
            // "Break" logic dependent on step
            loop {
                if step > 2 && random_test() {
                    return arg3;
                } // Exit 1 (Late)
                if random_test() {
                    break;
                } // Exit 2
            }
        }
        if step > 5 && random_test() {
            break;
        }
        step += 1;
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case58<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut count = 0;
    loop {
        if count < 3 {
            // Early iterations force p=arg2 and continue
            p = arg2;
            count += 1;
            continue;
        }
        break;
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case59<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut i = 0;
    loop {
        let mut j = 0;
        loop {
            let mut k = 0;
            loop {
                let mut l = 0;
                loop {
                    // Only assign in a specific "coordinate" in time
                    if i == 1 && j == 1 {
                        p = arg2;
                    }
                    if l > 0 && random_test() {
                        break;
                    }
                    l += 1;
                }
                if k > 0 && random_test() {
                    break;
                }
                k += 1;
            }
            if j > 1 && random_test() {
                break;
            }
            j += 1;
        }
        if i > 1 && random_test() {
            break;
        }
        i += 1;
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case60<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut ready_for_phase2 = false;

    // Loop 1
    loop {
        p = arg2; // Phase 1 alias
        ready_for_phase2 = true;
        if random_test() {
            break;
        }
    }

    // Loop 2
    loop {
        // Only assign arg3 if Phase 1 completed (always true topologically, but tests state tracking)
        if ready_for_phase2 && random_test() {
            p = arg3;
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,3)
fn case61<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut attempt = 0;
    'outer: loop {
        p = arg2; // Transient alias
        loop {
            // Only take the special break after attempts
            if attempt > 2 {
                p = arg3; // Final alias
                break 'outer;
            }
            if random_test() {
                break;
            }
        }
        attempt += 1;
    }
    p
}

/// Expected alias analysis result: (0,3),(0,4)
fn case62<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut stage = 0;
    'top: loop {
        p = arg2;
        loop {
            loop {
                if stage == 2 {
                    p = arg3;
                    break 'top;
                }
                if stage == 1 {
                    p = arg4;
                    break; // to middle
                }

                // Advance stage
                stage += 1;
            }
            break;
        }
        // implicit continue 'top
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
fn case63<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut c = 0;
    'block: loop {
        if c > 3 {
            p = arg2;
            break 'block;
        }
        if random_test() {
            c += 1;
            continue 'block;
        }
        break;
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case64<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut toggle = false;
    loop {
        // Toggle ensures both paths are taken over time
        match toggle {
            true => {
                p = arg2;
                break;
            }
            false => {
                p = arg3;
            }
        }

        toggle = !toggle; // Flip state

        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,4)
fn case65<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;
    let mut iter = 0;

    // Left Wing
    loop {
        if iter > 1 {
            p = arg3;
            break;
        }
        iter += 1;
    }

    // Reset iter logic for independent evolution or coupled? Let's use coupled.
    // Right Wing
    loop {
        if iter > 2 {
            q = arg4;
            break;
        } // Requires accumulation from Left Wing
        iter += 1;
    }

    // Merge
    if iter > 5 {
        p
    } else {
        q
    }
}

/// Expected alias analysis result: (0,4)
fn case66<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut state = 0;
    loop {
        match state {
            0 => p = arg2,
            1 => p = arg3,
            _ => p = arg4,
        }

        if state < 2 {
            state += 1;
        } else {
            if random_test() {
                break;
            }
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
fn case67<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;
    let mut i = 0;
    loop {
        // Only swap on even iterations
        if i % 2 == 0 {
            let temp = p;
            p = q;
            q = temp;
        }

        if i > 5 && random_test() {
            break;
        }
        i += 1;
    }
    p
}

/// Expected alias analysis result: (0,3)
fn case68<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut val = 0;
    loop {
        if val == 1 {
            p = arg2;
        } else if val == 2 {
            p = arg3;
        } else {
            // val 0: keep arg1
        }

        val += 1;
        if val > 3 {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case69<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut life = 0;
    loop {
        // Originally "if false", now "if life > 10" (needs deep unrolling)
        if life > 10 {
            p = arg2;
        }

        if life > 20 {
            break;
        }
        life += 1;
    }
    p
}

/// Expected alias analysis result: (0,4)
fn case70<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut outer_flag = false;
    loop {
        loop {
            // Inner loop toggles outer flag after delay
            match random_test() {
                true => p = arg2,
                false => p = arg3,
            }
            if random_test() {
                outer_flag = true;
                break;
            }
        }
        // arg4 only assigned if inner loop set the flag
        if outer_flag {
            p = arg4;
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,5)
fn case71<'a>(a: &'a i32, b: &'a i32, c: &'a i32, d: &'a i32, e: &'a i32) -> &'a i32 {
    let mut p = a;
    let mut noise_level = 0;
    loop {
        // Noise loops must run multiple times
        loop {
            if noise_level > 2 {
                break;
            }
            noise_level += 1;
        }

        // Actual assignment requires noise to be settled
        if noise_level > 2 {
            p = e;
        }

        break;
    }
    p
}

/// Expected alias analysis result: (0,5)
fn case72<'a>(a: &'a i32, b: &'a i32, c: &'a i32, d: &'a i32, e: &'a i32) -> &'a i32 {
    let mut p = a;
    let mut i = 0;
    loop {
        // Each iteration unlocks a new alias
        if i == 1 {
            p = b;
        }
        if i == 2 {
            p = c;
        }
        if i == 3 {
            p = d;
        }
        if i == 4 {
            p = e;
        }

        if i > 5 {
            break;
        }
        i += 1;
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case73<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg3;
    let mut tick = 0;

    loop {
        if tick % 2 == 0 {
            p = arg2;
        } else {
            q = arg4;
        }

        if tick > 3 {
            break;
        }
        tick += 1;
    }

    // Select based on final tick state
    if tick % 2 == 0 {
        p
    } else {
        q
    }
}

/// Expected alias analysis result: (0,3)
fn case74<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;
    let mut r = arg3;
    let mut step = 0;

    loop {
        if step > 0 {
            // Chain reaction delayed by step
            p = q; // Iter 1: p aliases arg2. Iter 2: p aliases r (arg3) because q became r
        }

        if step > 1 {
            q = r;
        }

        if step > 3 {
            break;
        }
        step += 1;
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case75<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut resets = 0;
    'outer: loop {
        p = arg2; // Transient
        loop {
            if resets < 3 {
                p = arg3; // Assignment happens
                resets += 1;
                continue 'outer; // But we reset execution to top
            }
            break;
        }
        break;
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case76<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut path_chosen = 0;

    if random_test() {
        p = arg2;
        path_chosen = 1;
    } else {
        p = arg3;
        path_chosen = 2;
    }

    // Shared Loop delays return and validates state
    let mut delay = 0;
    loop {
        // Analysis must preserve 'p' through this delay
        if delay > 2 && path_chosen > 0 {
            break;
        }
        delay += 1;
    }
    p
}

/// Expected alias analysis result: (0,1)
fn case77<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut i = 0;
    loop {
        p = arg2;
        if i == 1 {
            p = arg1; // Reset on 2nd iteration
            break;
        }
        if i > 5 {
            break;
        }
        i += 1;
    }
    p
}

/// Expected alias analysis result: (0,3)
fn case78<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut top_finished = false;

    loop {
        // Top Loop
        if random_test() {
            p = arg2;
            top_finished = true;
            break;
        }
    }

    match top_finished {
        true => {
            let mut bot_iter = 0;
            loop {
                // Bottom Loop - delayed assignment
                if bot_iter > 1 {
                    p = arg3;
                    break;
                }
                bot_iter += 1;
            }
        }
        false => {}
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case79<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut c = 0;
    'outer: loop {
        match c % 2 == 0 {
            true => {
                loop {
                    // Requires c to increment to be even/odd?
                    // Here we just use c to govern exit
                    if c == 2 {
                        p = arg2;
                        break 'outer;
                    } // Late exit

                    loop {
                        if c == 1 {
                            p = arg3;
                            break;
                        } // Mid update
                        break;
                    }
                    if random_test() {
                        break;
                    }
                }
            }
            false => {
                p = arg4;
            }
        }
        if c > 4 {
            break;
        }
        c += 1;
    }
    p
}
