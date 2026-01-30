#![feature(rustc_private)]
#![feature(box_patterns)]
#![feature(macro_metavar_expr_concat)]

#[macro_use]
pub mod utils;
pub mod analysis;
pub mod def_id;
pub mod preprocess;
extern crate intervals;
extern crate rustc_abi;
extern crate rustc_ast;
extern crate rustc_data_structures;
extern crate rustc_driver;
extern crate rustc_errors;
extern crate rustc_hir;
extern crate rustc_hir_pretty;
extern crate rustc_index;
extern crate rustc_infer;
extern crate rustc_interface;
extern crate rustc_metadata;
extern crate rustc_middle;
extern crate rustc_public;
extern crate rustc_session;
extern crate rustc_span;
extern crate rustc_target;
extern crate rustc_trait_selection;
extern crate rustc_traits;
extern crate rustc_type_ir;
extern crate thin_vec;
use crate::analysis::core::alias_analysis::{
    default::{STAliasAnalyzer, st_alias::STAnalyzer},
    mfp::MfpAliasAnalyzer,
};
use analysis::{
    Analysis,
    core::alias_analysis::{AliasAnalysis, FnAliasMapWrapper, default::AliasAnalyzer},
};
use rustc_ast::ast;
use rustc_driver::{Callbacks, Compilation};
use rustc_interface::{
    Config,
    interface::{self, Compiler},
};
use rustc_middle::{ty::TyCtxt, util::Providers};
use rustc_session::search_paths::PathKind;
use std::path::PathBuf;
use std::{env, sync::Arc};

// Insert rustc arguments at the beginning of the argument list that RAP wants to be
// set per default, for maximal validation power.
pub static RAP_DEFAULT_ARGS: &[&str] = &[
    "-Zalways-encode-mir",
    "-Zmir-opt-level=0",
    "-Zinline-mir-threshold=0",
    "-Zinline-mir-hint-threshold=0",
    "-Zcross-crate-inline-threshold=0",
];

/// This is the data structure to handle rapx options as a rustc callback.

#[derive(Debug, Clone, Hash)]
pub struct RapCallback {
    alias: bool,
    alias_mfp: bool,
    alias_st: bool,
    api_dependency: bool,
    callgraph: bool,
    dataflow: usize,
    ownedheap: bool,
    range: usize,
    ssa: bool,
    test: bool,
    infer: bool,
    opt: usize,
    rcanary: bool,
    safedrop: bool,
    show_mir: bool,
    show_mir_dot: bool,
    upg: usize,
    verify: bool,
    verify_std: bool,
    scan: bool,
    test_crate: Option<String>,
}

#[allow(clippy::derivable_impls)]
impl Default for RapCallback {
    fn default() -> Self {
        Self {
            alias: false,
            alias_mfp: false,
            alias_st: false,
            api_dependency: false,
            callgraph: false,
            dataflow: 0,
            ownedheap: false,
            range: 0,
            ssa: false,
            test: false,
            infer: false,
            opt: usize::MAX,
            rcanary: false,
            safedrop: false,
            show_mir: false,
            show_mir_dot: false,
            upg: 0,
            verify: false,
            verify_std: false,
            scan: false,
            test_crate: None,
        }
    }
}

impl Callbacks for RapCallback {
    fn config(&mut self, config: &mut Config) {
        config.override_queries = Some(|_, providers| {
            providers.extern_queries.used_crate_source = |tcx, cnum| {
                let mut providers = Providers::default();
                rustc_metadata::provide(&mut providers);
                let mut crate_source = (providers.extern_queries.used_crate_source)(tcx, cnum);
                // HACK: rustc will emit "crate ... required to be available in rlib format, but
                // was not found in this form" errors once we use `tcx.dependency_formats()` if
                // there's no rlib provided, so setting a dummy path here to workaround those errors.
                Arc::make_mut(&mut crate_source).rlib = Some((PathBuf::new(), PathKind::All));
                crate_source
            };
        });
    }

    fn after_crate_root_parsing(
        &mut self,
        compiler: &interface::Compiler,
        krate: &mut ast::Crate,
    ) -> Compilation {
        let build_std = compiler
            .sess
            .opts
            .crate_name
            .as_deref()
            .map(|s| matches!(s, "core" | "std"))
            .unwrap_or(false);
        preprocess::dummy_fns::create_dummy_fns(krate, build_std);
        preprocess::ssa_preprocess::create_ssa_struct(krate, build_std);
        Compilation::Continue
    }
    fn after_analysis<'tcx>(&mut self, _compiler: &Compiler, tcx: TyCtxt<'tcx>) -> Compilation {
        rap_trace!("Execute after_analysis() of compiler callbacks");

        rustc_public::rustc_internal::run(tcx, || {
            def_id::init(tcx);
            if self.is_building_test_crate() {
                start_analyzer(tcx, self);
            } else {
                let package_name = std::env::var("CARGO_PKG_NAME")
                    .expect("cannot capture env var `CARGO_PKG_NAME`");
                rap_trace!("skip analyzing package `{}`", package_name);
            }
        })
        .expect("Failed to run rustc_public.");
        rap_trace!("analysis done");

        Compilation::Continue
    }
}

impl RapCallback {
    fn is_building_test_crate(&self) -> bool {
        match &self.test_crate {
            None => true,
            Some(test_crate) => {
                let test_crate: &str = test_crate;
                let package_name = std::env::var("CARGO_PKG_NAME")
                    .expect("cannot capture env var `CARGO_PKG_NAME`");
                package_name == test_crate
            }
        }
    }

    /// Enable alias analysis. The parameter is used to config the threshold of alias analysis.
    /// Currently, we mainly use it to control the depth of field-sensitive analysis.
    /// -alias0: set field depth limit to 10; do not distinguish different flows within a each
    /// strongly-connected component.
    /// -alias1: set field depth limit to 20 (this is default setting).
    /// -alias2: set field depth limit to 30.
    pub fn enable_alias(&mut self, arg: String) {
        self.alias = true;
        match arg.as_str() {
            "-alias" => unsafe {
                env::set_var("ALIAS", "1");
            },
            "-alias0" => unsafe {
                env::set_var("ALIAS", "0");
            },
            "-alias1" => unsafe {
                env::set_var("ALIAS", "1");
            },
            "-alias2" => unsafe {
                env::set_var("ALIAS", "2");
            },
            _ => {}
        }
    }

    /// Test if alias analysis is enabled.
    pub fn is_alias_enabled(&self) -> bool {
        self.alias
    }

    pub fn enable_alias_mfp(&mut self) {
        self.alias_mfp = true;
    }

    pub fn is_alias_mfp_enabled(&self) -> bool {
        self.alias_mfp
    }

    pub fn enable_alias_st(&mut self) {
        self.alias_st = true;
    }

    pub fn is_alias_st_enabled(&self) -> bool {
        self.alias_st
    }

    /// Enable API-dependency graph generation.
    pub fn enable_api_dependency(&mut self) {
        self.api_dependency = true;
    }

    /// Test if API-dependency graph generation is enabled.
    pub fn is_api_dependency_enabled(&self) -> bool {
        self.api_dependency
    }

    /// Enable call-graph analysis.
    pub fn enable_callgraph(&mut self) {
        self.callgraph = true;
    }

    /// Test if call-graph analysis is enabled.
    pub fn is_callgraph_enabled(&self) -> bool {
        self.callgraph
    }

    /// Enable owned heap analysis.
    pub fn enable_ownedheap(&mut self) {
        self.ownedheap = true;
    }

    /// Test if owned-heap analysis is enabled.
    pub fn is_ownedheap_enabled(&self) -> bool {
        self.ownedheap
    }

    /// Enable dataflow analysis.
    pub fn enable_dataflow(&mut self, x: usize) {
        self.dataflow = x;
    }

    /// Test if dataflow analysis is enabled.
    pub fn is_dataflow_enabled(&self) -> usize {
        self.dataflow
    }

    /// Enable range analysis.
    pub fn enable_range_analysis(&mut self, x: usize) {
        self.range = x;
    }

    /// Test if range analysis is enabled.
    pub fn is_range_analysis_enabled(&self) -> bool {
        self.range > 0
    }

    /// Enable test of features provided by the core analysis traits.
    pub fn enable_test(&mut self) {
        self.test = true;
    }

    /// Check if test is enabled.
    pub fn is_test_enabled(&self) -> bool {
        self.test
    }

    /// Enable ssa transformation
    pub fn enable_ssa_transform(&mut self) {
        self.ssa = true;
    }

    /// Test if ssa transformation is enabled.
    pub fn is_ssa_transform_enabled(&self) -> bool {
        self.ssa
    }

    /// Enable optimization analysis for performance bug detection.
    pub fn enable_opt(&mut self, x: usize) {
        self.opt = x;
    }

    /// Test if optimization analysis is enabled.
    pub fn is_opt_enabled(&self) -> usize {
        self.opt
    }

    /// Enable rcanary for memory leakage detection.
    pub fn enable_rcanary(&mut self) {
        self.rcanary = true;
    }

    /// Test if rcanary is enabled.
    pub fn is_rcanary_enabled(&self) -> bool {
        self.rcanary
    }

    /// Enable safedrop for use-after-free bug detection.
    /// Similar to alias analysis, the second parameter is to control the depth threshold for
    /// field-sensitive analysis.
    pub fn enable_safedrop(&mut self, arg: String) {
        self.safedrop = true;
        match arg.as_str() {
            "-F" => {
                unsafe {
                    env::set_var("SAFEDROP", "1");
                }
                unsafe {
                    env::set_var("MOP", "1");
                }
            }
            "-F0" => {
                unsafe {
                    env::set_var("SAFEDROP", "0");
                }
                unsafe {
                    env::set_var("MOP", "0");
                }
            }
            "-F1" => {
                unsafe {
                    env::set_var("SAFEDROP", "1");
                }
                unsafe {
                    env::set_var("MOP", "1");
                }
            }
            "-F2" => {
                unsafe {
                    env::set_var("SAFEDROP", "2");
                }
                unsafe {
                    env::set_var("MOP", "2");
                }
            }
            "-uaf" => {
                unsafe {
                    env::set_var("SAFEDROP", "1");
                }
                unsafe {
                    env::set_var("MOP", "1");
                }
            }
            _ => {}
        }
    }

    /// Test if safedrop is enabled.
    pub fn is_safedrop_enabled(&self) -> bool {
        self.safedrop
    }

    /// Enable mir display.
    pub fn enable_show_mir(&mut self) {
        self.show_mir = true;
    }

    /// Test if mir display is enabled.
    pub fn is_show_mir_enabled(&self) -> bool {
        self.show_mir
    }

    pub fn enable_show_mir_dot(&mut self) {
        self.show_mir_dot = true;
    }

    pub fn is_show_mir_dot_enabled(&self) -> bool {
        self.show_mir_dot
    }

    pub fn enable_upg(&mut self, x: usize) {
        self.upg = x;
    }

    pub fn is_upg_enabled(&self) -> usize {
        self.upg
    }

    pub fn enable_verify(&mut self) {
        self.verify = true;
    }

    pub fn is_verify_enabled(&self) -> bool {
        self.verify
    }

    pub fn enable_verify_std(&mut self) {
        self.verify_std = true;
    }

    pub fn is_verify_std_enabled(&self) -> bool {
        self.verify_std
    }

    pub fn enable_infer(&mut self) {
        self.infer = true;
    }

    pub fn is_infer_enabled(&self) -> bool {
        self.infer
    }

    pub fn enable_scan(&mut self) {
        self.scan = true;
    }

    pub fn is_scan_enabled(&self) -> bool {
        self.scan
    }

    pub fn set_test_crate(&mut self, crate_name: impl ToString) {
        self.test_crate = Some(crate_name.to_string())
    }
}

/// Start the analysis with the features enabled.
pub fn start_analyzer(tcx: TyCtxt, callback: &RapCallback) {
    if callback.is_alias_enabled() {
        let mut analyzer = AliasAnalyzer::new(tcx);
        let duration = std::time::Instant::now();
        analyzer.run();
        rap_info!(
            "Alias analysis via STA finished in {:?}.",
            duration.elapsed()
        );
        let alias = analyzer.get_local_fn_alias();
        for (def_id, result) in alias {
            let fn_name = tcx.def_path_str(def_id);
            rap_info!("Alias of {:?}: {}", fn_name, result);
        }
    }

    if callback.is_alias_mfp_enabled() {
        let mut analyzer = MfpAliasAnalyzer::new(tcx);
        let duration = std::time::Instant::now();
        analyzer.run();
        rap_info!(
            "Alias analysis via mfp finished in {:?}.",
            duration.elapsed()
        );
        let alias = analyzer.get_local_fn_alias();
        for (def_id, result) in alias {
            let fn_name = tcx.def_path_str(def_id);
            rap_info!("Alias of {:?}: {}", fn_name, result);
        }
    }

    if callback.is_alias_st_enabled() {
        let mut analyzer = STAliasAnalyzer::new(tcx);
        analyzer.run();
        let alias = analyzer.get_local_fn_alias();
        rap_info!("{}", FnAliasMapWrapper(alias));
    }
}
