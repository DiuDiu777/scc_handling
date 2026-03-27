// Common enums used across benchmarks to drive state logic
#[derive(PartialEq, Clone, Copy)]
pub enum LoopState {
    Start,
    Processing,
    Finishing,
    Done,
}

#[derive(PartialEq, Clone, Copy)]
pub enum BranchMode {
    PathA,
    PathB,
    PathC,
    DeadPath, // Used for logical exclusion
}

enum State {
    Load,
    Process,
    Finish,
}

enum Selector {
    First,
    Second,
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Selector_test2 {
    First,
    Second,
    Third,
    Fourth,
}

enum Mode {
    Read,
    Write,
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Flag {
    A,
    B,
    C,
}

fn random_test() -> bool {
    use std::time::{SystemTime, UNIX_EPOCH};
    let start = SystemTime::now();
    let since_the_epoch = start
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards");
    since_the_epoch.subsec_nanos() % 2 == 0
}

/// Expected alias analysis result: (0, 2), (0, 3)
pub fn case_1<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, start_state: LoopState) -> &'a i32 {
    let mut res = p3;
    let mut state = start_state;

    loop {
        // Outer loop logic
        if state == LoopState::Start {
            res = p1;
            state = LoopState::Processing;

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
            }
        }

        if state == LoopState::Finishing || state == LoopState::Done {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 3), (1, 3)
pub fn case_2<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, enable_mutation: bool) -> &'a i32 {
    let mut res = p2;
    let mut steps = 0;

    loop {
        res = *p1;
        steps += 1;

        loop {
            // Inner loop constraint: Only mutate if flag is set AND steps > 0
            if enable_mutation && steps > 0 {
                *p1 = p3;
                res = p3;
            }

            if steps >= 2 {
                break;
            }
            steps += 1;
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
    let mut depth = 0;

    loop {
        loop {
            loop {
                if let BranchMode::DeadPath = mode {
                    res = p2;
                }
                if depth > 0 {
                    break;
                }
                depth += 1;
            }
            if let BranchMode::PathA = mode {
                res = p3;
            }
            if depth > 1 {
                break;
            }
            depth += 1;
        }
        if depth > 2 {
            break;
        }
        depth += 1;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2)
pub fn case_4<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, guard: bool) -> &'a i32 {
    let mut res = p1;
    let mut i = 0;

    loop {
        if guard {
            let mut inner_ptr = p3;
            loop {
                // Deterministic assignment
                inner_ptr = p2;
                if i >= 1 {
                    break;
                }
                i += 1;
            }
            res = inner_ptr;
        }

        // Deep Conflict: If guard is false, res cannot be p2 or p3.
        if i >= 1 || !guard {
            break;
        }
        i += 1;
    }
    res
}

/// Expected alias analysis result: (0, 3), (0, 4)
pub fn case_5<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, iter_max: i32) -> &'a i32 {
    let mut res = p1;
    let mut outer_i = 0;

    loop {
        let mut temp = res;
        let mut inner_i = 0;

        loop {
            if (outer_i + inner_i) % 2 == 0 {
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

        if outer_i == iter_max {
            res = p4;
        }

        if outer_i >= 2 {
            break;
        }
        outer_i += 1;
    }
    res
}

/// Expected alias analysis result:(0,5),(1,2),(0,2)
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

    loop {
        if swap_mode {
            loop {
                if i % 2 == 0 {
                    *p1 = p2;
                } else {
                    *p1 = p3;
                }
                if i > 0 {
                    break;
                }
                i += 1;
            }
            res = *p1;
        } else {
            res = p5;
        }
        if i >= 2 || !swap_mode {
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
            if counter == limit {
                res = p2;
                break 'outer;
            }
            if counter > limit {
                res = p3;
                break;
            }
            counter += 1;
            if counter > 5 {
                break 'outer;
            } // Safety break
        }
        break; // Implicit outer break
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2)
pub fn case_8<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, flag: bool) -> &'a i32 {
    let mut res = p3;
    let mut once = false;

    loop {
        if flag {
            res = p1;
        }

        loop {
            // Logical Pruning: If flag is TRUE, we skip p2 assignment to avoid overwrite?
            // Or here we define: if !flag, we assign p2.
            if !flag {
                res = p2;
            }
            break; // Single pass inner
        }

        if once {
            break;
        }
        once = true;
    }
    res
}

/// Expected alias analysis result:(0, 3), (1, 3)
pub fn case_9<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p2;
    let mut i = 0;
    loop {
        let mut j = 0;
        loop {
            let mut k = 0;
            loop {
                // Deepest level update
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

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_10<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, mode: BranchMode) -> &'a i32 {
    let mut res = p3;
    loop {
        if let BranchMode::PathA = mode {
            return p1;
        }
        if let BranchMode::PathB = mode {
            res = p2;
            break;
        }
        // If PathC, returns p3 (original res) after break
        break;
    }
    res
}

/// Expected alias analysis result: (0, 3)
pub fn case_11<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, iterations: i32) -> &'a i32 {
    let mut res = p1;
    let mut i = 0;

    loop {
        if i < iterations {
            res = p2;
            i += 1;
            continue; // Cycles back with res=p2
        }
        if i >= iterations {
            res = p3;
            break;
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4)
pub fn case_12<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, x: i32) -> &'a i32 {
    loop {
        if x == 1 {
            return p1;
        }
        if x > 5 {
            if x > 10 {
                return p2;
            }
            let _unused = p3;

            if x == 6 {
                return p4;
            } // Added deterministic exit
            break;
        }
        if x == 0 {
            return p4;
        }
        break;
    }
    // Fallback return if loop breaks
    p3
}

/// Expected alias analysis result:(0, 2), (0, 3), (1, 2)
pub fn case_13<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, do_alias: bool) -> &'a i32 {
    loop {
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
    let constant_val = 10;
    loop {
        if constant_val == 10 {
            res = p2;
            break;
        }
        // PRUNING: This block is logically unreachable.
        if constant_val == 20 {
            return p3;
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4)
pub fn case_15<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, selector: i32) -> &'a i32 {
    let mut res = p1;
    loop {
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
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 3)
pub fn case_16<'a>(p1: &'a i32, _p2: &'a i32, p3: &'a i32, condition: bool) -> &'a i32 {
    loop {
        if condition {
            return p1;
        } else {
            return p3;
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
        if i < 0 {
            // Unreachable check
            return res;
        }
        i += 1;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_18<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, mode: BranchMode) -> &'a i32 {
    let mut res = p1;
    loop {
        match mode {
            BranchMode::PathA => {
                res = p2;
                // Loops back with p2
            }
            BranchMode::PathB => {
                return res;
            }
            _ => {
                return p3;
            }
        }
        // If PathA, we hit here. To prevent infinite loop in benchmark:
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 3)
pub fn case_19<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, input_flag: bool) -> &'a i32 {
    let mut res = p1;
    let mut intermediate_state = false;

    // Sibling A
    loop {
        if input_flag {
            res = p2;
            intermediate_state = true;
        }
        break;
    }

    // Sibling B
    loop {
        // Constraint: We only pick p3 if Sibling A set the state (Correlated)
        if intermediate_state {
            res = p3;
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
    // Sibling B
    loop {
        if do_write {
            res = *p1; // Reads p2 (if written) or original p1
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4)
pub fn case_21<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, step: i32) -> &'a i32 {
    let mut res = p1;
    // Loop 1
    loop {
        if step == 1 {
            res = p2;
        }
        break;
    }
    // Loop 2
    loop {
        if step == 2 {
            res = p3;
        }
        break;
    }
    // Loop 3
    loop {
        if step == 3 {
            res = p4;
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_22<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, run_b: bool) -> &'a i32 {
    let mut res = p1;
    // Loop A
    loop {
        res = p2;
        break;
    }

    if run_b {
        // Loop B
        loop {
            res = p3;
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_23<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, use_temp1: bool) -> &'a i32 {
    let mut temp1 = p1;
    // Loop A
    loop {
        temp1 = p2;
        break;
    }

    let temp2 = p3;
    // Loop B (Empty logic for benchmark structure)
    loop {
        break;
    }

    if use_temp1 {
        temp1
    } else {
        temp2
    }
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4)
pub fn case_24<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, mode: i32) -> &'a i32 {
    let mut res = p1;
    // Loop A
    loop {
        if mode == 1 {
            res = p2;
        }
        break;
    }
    // Loop B
    loop {
        // Correlated: If mode == 1, we entered A.
        // If mode == 2, we enter B branch 1.
        if mode == 2 {
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
    mode: i32,
) -> &'a i32 {
    let mut res = p1;
    loop {
        match mode {
            2 => res = p2,
            3 => res = p3,
            4 => res = p4,
            5 => res = p5,
            _ => (), // Keep p1
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3), (0, 4), (1, 3)
pub fn case_26<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, path: i32) -> &'a i32 {
    let mut res = p4;
    loop {
        if path == 1 {
            res = p2;
        } else if path == 2 {
            *p1 = p3;
            res = *p1;
        } else {
            res = p4;
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4)
pub fn case_27<'a>(
    p1: &'a i32,
    p2: &'a i32,
    p3: &'a i32,
    p4: &'a i32,
    x: bool,
    y: bool,
) -> &'a i32 {
    let mut res = p1;
    loop {
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
            // else keep p1
        }
        break;
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_28<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, idx: i32) -> &'a i32 {
    let mut res = p1;
    loop {
        // Multiple paths converge to p2
        if idx == 0 {
            res = p2;
        } else if idx == 1 {
            res = p2;
        } else if idx == 2 {
            res = p2;
        } else {
            res = p3;
        }
        break;
    }
    // p4 is never reachable
    res
}

/// Expected alias analysis result:(0, 2), (0, 3), (0, 4)
pub fn case_29<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, val: i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if val < 0 {
            res = p2;
        } else if val == 0 {
            return p3;
        } else if val > 0 {
            res = p4;
            break;
        }
        // Fallthrough (val < 0)
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (1, 3)
pub fn case_30<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, mode: BranchMode) -> &'a i32 {
    let mut res = p2;
    loop {
        match mode {
            BranchMode::PathA => res = *p1,
            BranchMode::PathB => {
                *p1 = p3;
                res = p2;
            }
            BranchMode::PathC => res = p3,
            _ => (),
        }
        break;
    }
    res
}

/// Expected alias analysis result: (0,1)
fn case_31<'a>(x: &'a i32, y: &'a i32, choice: Selector) -> &'a i32 {
    let mut r = x;
    while *r > 1 {
        let a = match choice {
            Selector::First => x,
            Selector::Second => y,
        };
        r = match choice {
            Selector::First => a,
            Selector::Second => x,
        };
    }
    return r;
}

/// Expected alias analysis result: (0,1)
fn case_32(x: *mut i32, y: *mut i32, choice: Selector) -> *mut i32 {
    let mut r = x;

    unsafe {
        while *r > 0 {
            // (p,x) or (p,y)
            let mut p = match choice {
                Selector::First => y,
                Selector::Second => x,
            };

            loop {
                let q = match choice {
                    Selector::First => x,
                    Selector::Second => p,
                };

                *q -= 1;
                r = q;

                if *r <= 1 {
                    break;
                }
            }

            if *r == 0 {
                break;
            }
        }
    }
    r
}

/// Expected alias analysis result: (0,1)
fn case_33(x: *mut i32, y: *mut i32, choice: Selector) -> *mut i32 {
    let mut r = x;

    unsafe {
        while *r > 0 {
            // (p,x) or (p,y)
            let mut p = match choice {
                Selector::First => y,
                Selector::Second => x,
            };

            loop {
                let q = match choice {
                    Selector::First => x,
                    Selector::Second => p,
                };

                r = q;

                if random_test() {
                    break;
                }
            }

            if random_test() {
                break;
            }
        }
    }
    r
}

/// Expected alias analysis result: (0,1)
fn case_34<'a>(x: &'a i32, y: &'a i32, choice: Selector) -> &'a i32 {
    let mut r = x;

    while *r > 0 {
        let mut p = match choice {
            Selector::First => y,
            Selector::Second => x,
        };

        loop {
            if random_test() {
                break;
            }
            // Correlated Branch:
            let q = match choice {
                Selector::First => x,
                Selector::Second => p,
            };

            r = q;
        }
        if random_test() {
            break;
        }
    }
    r
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_35(x: *mut i32, y: *mut i32, choice: Selector) -> *mut i32 {
    let mut r = x;
    let mut q = x;

    unsafe {
        while *r > 0 {
            let mut p = match choice {
                Selector::First => y,
                Selector::Second => x,
            };

            loop {
                r = q;
                q = match choice {
                    Selector::First => x,
                    Selector::Second => p,
                };
                *q -= 1;
                if *r <= 1 {
                    break;
                }
                q = y;
            }

            if *r == 0 {
                break;
            }
        }
    }
    r
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_36<'a>(x: &'a i32, y: &'a i32, mode: Mode) -> &'a i32 {
    let mut p = x;
    loop {
        // Constraint: mode is invariant
        let temp = match mode {
            Mode::Read => x,
            Mode::Write => y,
        };

        p = match mode {
            Mode::Read => temp,
            Mode::Write => y,
        };
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1)
fn case_37<'a>(x: &'a i32, y: &'a i32, mode: Mode) -> &'a i32 {
    let mut p = x;
    // Outer loop
    while random_test() {
        let target = match mode {
            Mode::Read => x,
            Mode::Write => y,
        };
        for _ in 0..10 {
            p = match mode {
                Mode::Read => target,
                Mode::Write => x,
            };
        }
    }
    p
}

/// Expected alias analysis result: (0,1)
fn case_38<'a>(x: &'a i32, y: &'a i32, mode: i32) -> &'a i32 {
    let mut r = x;
    loop {
        let mut temp = x;
        if mode == 1 {
            temp = y;
        }
        if mode == 1 {
            r = x;
        } else {
            r = temp;
        }

        if random_test() {
            break;
        }
    }
    r
}

/// Expected alias analysis result: (0,1)
fn case_39<'a>(x: &'a i32, y: &'a i32, mode: bool) -> &'a i32 {
    let mut p = x;

    loop {
        if mode {
            p = y;
        } else {
            return p;
        }

        if random_test() {
            break;
        }
    }

    // Fallback return (for safety)
    x
}

/// Expected alias analysis result: (0,1),(0,2)
pub fn case_40<'a>(x: &'a i32, y: &'a i32, cond: bool) -> &'a i32 {
    let mut p = x; // p -> 1
    loop {
        if cond {
            p = y; // p -> 2
        }

        if cond {
            return p; // returns 2 (y)
        } else {
            return p; // returns 1 (x)
        }
    }
}

/// Expected alias analysis result: (0,1)
pub fn case_41<'a>(x: &'a i32, y: &'a i32, cond: bool) -> &'a i32 {
    let mut p = x;
    loop {
        if cond {
            p = y;
        }

        // If cond is true, we cannot take this branch to escape with y
        if !cond {
            break;
        }

        // Forced exit to prevent infinite loop analysis issues, returning x
        if random_test() {
            p = x;
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
pub fn case_42<'a>(x: &'a i32, y: &'a i32, z: &'a i32, flag: Flag) -> &'a i32 {
    let mut p = x;
    loop {
        match flag {
            Flag::A => p = x,
            Flag::B => p = y,
            Flag::C => p = z,
        }

        // Correlated check
        match flag {
            Flag::A => return p, // Returns x
            Flag::B => break,    // Breaks with y
            Flag::C => {}        // Loops with z (becomes infinite or hits random break)
        }

        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
pub fn case_43<'a>(x: &'a i32, y: &'a i32, z: &'a i32, c: bool) -> &'a i32 {
    let mut p = z; // Default
    loop {
        if c {
            if random_test() {
                p = x;
            } else {
                p = y;
            }
            break;
        }
        // If !c, p stays z
        break;
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
pub fn case_44<'a>(x: &'a i32, y: &'a i32) -> &'a i32 {
    let mut p = x;
    let mut state = true;
    loop {
        if state {
            p = x;
        } else {
            p = y;
        }
        state = !state;
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
pub fn case_45<'a>(x: &'a i32, y: &'a i32, replace: bool) -> &'a i32 {
    let mut p = x;
    loop {
        if replace {
            p = y;
        }
        // If !replace, p stays x (or previous value)
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,2)
pub fn case_46<'a>(x: &'a i32, y: &'a i32, z: &'a i32) -> &'a i32 {
    let mut p = x;
    let k = 5;
    loop {
        if k > 10 {
            p = z; // Unreachable
        } else {
            p = y;
        }
        break;
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
pub fn case_47<'a>(x: &'a i32, y: &'a i32, use_x: bool) -> &'a i32 {
    let mut p = y;
    let mut i = 0;
    while i < 1 {
        if use_x {
            p = x;
        } else {
            p = y;
        }
        i += 1;
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
pub fn case_48<'a>(x: &'a i32, y: &'a i32, z: &'a i32) -> &'a i32 {
    let mut p = x;
    loop {
        if random_test() {
            p = y;
        } else {
            p = z;
        }

        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
pub fn case_49<'a>(x: &'a i32, y: &'a i32, flag: bool) -> &'a i32 {
    let mut p = x;
    loop {
        if !flag {
            p = y;
            break;
        }
        break;
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
pub fn case_50<'a>(x: &'a i32, y: &'a i32, z: &'a i32, mode: i32) -> &'a i32 {
    let mut p = z;
    loop {
        // Block 1: Setup
        if mode == 1 {
            p = x;
        } else if mode == 2 {
            p = y;
        }

        if random_test() {
            break;
        }

        if mode == 1 || mode == 2 {
            return p;
        }

        break;
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
pub fn case_51<'a>(x: &'a i32, y: &'a i32, z: &'a i32) -> &'a i32 {
    let mut p = z;
    'outer: loop {
        if random_test() {
            p = y;
            break 'outer;
        }
        loop {
            if random_test() {
                p = x;
                break 'outer;
            }
            if random_test() {
                break;
            } // Back to outer
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
pub fn case_52<'a>(x: &'a i32, y: &'a i32, z: &'a i32, a: bool, b: bool) -> &'a i32 {
    let mut p = z;
    loop {
        if a {
            p = x;
        } else if b {
            p = y;
        }

        // Guard: return only if we set it to x or y
        if a || b {
            return p;
        }

        // If neither, return z
        return p;
    }
}

/// Expected alias analysis result: (0,2)
pub fn case_53<'a>(x: &'a i32, y: &'a i32) -> &'a i32 {
    let mut p = x;
    let mut i = 0;
    loop {
        if i == 0 {
            p = x;
        } else if i == 1 {
            p = y;
        } else {
            return p; // Returns y because i must be >= 2 here
        }

        i += 1;
        if i > 2 {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
pub fn case_54<'a>(x: &'a i32, y: &'a i32, z: &'a i32, c1: bool, c2: bool) -> &'a i32 {
    let mut p = x;

    // Outer Loop
    loop {
        // Correlated Branch 1
        if c1 {
            p = y;
        }

        // Inner Loop
        loop {
            // Loop carried dependency: p points to z on subsequent inner iters
            if random_test() {
                p = z;
            }

            if !c1 {
                if c2 {
                    return x;
                } // Explicit return x
            }

            if random_test() {
                break;
            }
        }

        if c1 {
            return p;
        }

        return p;
    }
}

/// Expected alias analysis result: (0,1),(0,3)
fn case_55<'a>(x: &'a i32, y: &'a i32, z: &'a i32, use_x: bool) -> &'a i32 {
    let mut p = z; // Default to 3

    // Loop 1: Conditional Initialization
    // Although in a loop, the condition is loop-invariant
    while random_test() {
        if use_x {
            p = x; // p -> 1
        } else {
            p = y; // p -> 2
        }
        if random_test() {
            break;
        }
    }

    // Loop 2: Correlated Exit
    loop {
        if use_x {
            return p;
        } else {
            return z;
        }
    }
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_56<'a>(a: &'a i32, b: &'a i32) -> &'a i32 {
    let mut cursor = a; // Init: cursor -> 1
    let mut first_iter = true;

    loop {
        // If we break immediately (0 iterations logic), we return a.
        if random_test() {
            break;
        }

        if !first_iter {
            // On 2nd+ iteration, cursor points to b.
            cursor = b;
        }

        first_iter = false;

        // Loop-carried dependency: cursor's value flows back to top
    }

    cursor
}

/// Expected alias analysis result: (0,1),(0,3)
fn case_57<'a>(a: &'a i32, b: &'a i32, c: &'a i32, condition: bool) -> &'a i32 {
    let mut r = a; // r -> 1

    loop {
        // Outer SCC
        if condition {
            r = c; // r -> 3
            break;
        }

        // We only reach here if !condition
        loop {
            // Inner SCC
            if condition {
                r = b;
            }
            if random_test() {
                break;
            }
        }
        break;
    }

    r
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_58<'a>(x: &'a i32, y: &'a i32) -> &'a i32 {
    let mut p = x; // p -> 1
    let mut q = y; // q -> 2

    while random_test() {
        let temp = p;
        p = q;
        q = temp;
    }

    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_59<'a>(a: &'a i32, b: &'a i32, c: &'a i32) -> &'a i32 {
    let mut acc = a; // acc -> 1

    loop {
        let choice = random_test();

        if choice {
            // Exit A: Return current accumulator
            return acc;
        }

        if random_test() {
            // Exit B: Set to b and break (returns b eventually)
            acc = b;
            break;
        }

        // Loop Continuation: Set to c and loop again
        acc = c;
    }

    acc
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_60<'a>(x: &'a i32, y: &'a i32, z: &'a i32, choice: Selector_test2) -> &'a i32 {
    let mut r = x;
    let mut p = match choice {
        Selector_test2::First => y,
        Selector_test2::Second => x,
        _ => z,
    };
    let mut stage = 0;

    loop {
        if random_test() {
            break;
        }

        // Correlated Guard: Only enter if choice is Second
        if let Selector_test2::Second = choice {
            if stage > 0 {
                p = z; // Only reachable in Iter 2+ AND if choice == Second
            }
        }

        r = p;
        stage += 1;
    }

    r
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_61<'a>(a: &'a i32, b: &'a i32, c: &'a i32) -> &'a i32 {
    let mut temp = a;
    let mut flag = false;

    // Loop A: Decides whether temp switches to b
    loop {
        if random_test() {
            temp = b;
            flag = true;
            break;
        }
        if random_test() {
            break;
        }
    }

    let mut res = c;

    // Loop B: Consumes temp based on flag
    loop {
        if flag {
            res = temp; // Can be b (if flag=true)
        } else {
            res = a; // Can be a (if flag=false, temp remained a)
        }

        // Loop-carried: if we loop again, res might become c
        if random_test() {
            res = c;
        }
        if random_test() {
            break;
        }
    }
    res
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_62<'a>(a: &'a i32, b: &'a i32) -> &'a i32 {
    let mut p = a;
    let mut q = b;

    loop {
        if random_test() {
            break;
        }

        let temp = p;
        p = q;
        q = temp;
    }
    p
}

/// Expected alias analysis result: (0,1)
fn case_63<'a>(x: &'a i32, y: &'a i32, choice: Selector_test2) -> &'a i32 {
    let mut r = x;
    loop {
        match choice {
            Selector_test2::First => {
                // Path A
                let mut inner = x;
                loop {
                    if random_test() {
                        break;
                    }
                    // Inner check for Second (Impossible if context is First)
                    if let Selector_test2::Second = choice {
                        inner = y; // UNREACHABLE
                    }
                }
                r = inner;
            }
            Selector_test2::Second => {
                r = x;
            }
            _ => {
                r = x;
            }
        }
        if random_test() {
            break;
        }
    }
    r
}

/// Expected alias analysis result: (0,1),(0,2),(0,3),(0,4)
fn case_64<'a>(a: &'a i32, b: &'a i32, c: &'a i32, d: &'a i32) -> &'a i32 {
    let mut p = a;
    let mut counter = 0;

    loop {
        if counter == 0 {
            p = b;
        } else if counter == 1 {
            p = c;
        } else {
            p = d;
        }

        if random_test() {
            return p; // Exit 1: Returns current state
        }

        if random_test() {
            p = a; // Reset
            break; // Exit 2: Returns a
        }

        counter += 1;
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_65<'a>(base: &'a i32, target: &'a i32, dummy: &'a i32) -> &'a i32 {
    let mut r = base;
    let mut active = false;

    loop {
        // L1
        loop {
            // L2
            loop {
                // L3
                loop {
                    // L4
                    if active {
                        r = target; // Reachable only after active becomes true
                    } else {
                        r = base;
                    }

                    if random_test() {
                        break;
                    }
                    active = true; // State change deep inside
                }
                if random_test() {
                    break;
                }
            }
            if random_test() {
                break;
            }
        }
        if random_test() {
            break;
        }
        // Loop carried: active remains true for next outer iteration
        if !active {
            r = dummy;
        } // Reachable in first iter before deep dive
    }
    r
}

/// Expected alias analysis result: (0,1),(0,2),(0,3),(0,4),(0,5),(0,6)
fn case_66<'a>(
    a1: &'a i32,
    a2: &'a i32,
    a3: &'a i32,
    a4: &'a i32,
    a5: &'a i32,
    a6: &'a i32,
    index: usize,
) -> &'a i32 {
    let mut r = a1;
    let mut idx = index;

    loop {
        r = match idx % 6 {
            0 => a1,
            1 => a2,
            2 => a3,
            3 => a4,
            4 => a5,
            _ => a6,
        };

        if random_test() {
            break;
        }
        idx += 1; // Loop-carried dependency on index
    }
    r
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_67<'a>(x: &'a i32, y: &'a i32, mode: bool) -> &'a i32 {
    let mut p = x;
    loop {
        if mode {
            p = y;
            if random_test() {
                break;
            } // Exit with y
        } else {
            p = x;
            if random_test() {
                break;
            } // Exit with x
        }

        // Noise
        p = x;
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_68<'a>(a: &'a i32, b: &'a i32) -> &'a i32 {
    // tuple.0 is data, tuple.1 is next
    let mut t = (a, b);

    loop {
        if random_test() {
            break;
        }
        // Swap fields
        t = (t.1, t.0);
    }
    t.0
}

/// Expected alias analysis result: (0,3)
fn case_69<'a>(x: &'a i32, y: &'a i32, z: &'a i32) -> &'a i32 {
    let mut res = x;
    let mut outer_p = y;

    loop {
        res = outer_p; // res -> y

        loop {
            let mut inner_p = z;
            if random_test() {
                res = inner_p; // res -> z
                break;
            }
            inner_p = x; // Noise
        }

        if random_test() {
            break;
        }
        outer_p = x; // Loop carried: outer_p becomes x
    }
    res
}

/// Expected alias analysis result: (0,1), (0,2)
fn case_70<'a>(x: &'a i32, y: &'a i32) -> &'a i32 {
    let mut r = x;
    let mut latched = false;

    loop {
        if latched {
            r = y;
        } else {
            r = x;
        }

        if random_test() {
            latched = true;
        }

        if latched && random_test() {
            break;
        }
    }
    r
}

/// Expected alias analysis result: (0,4)
fn case_71<'a>(a: &'a i32, b: &'a i32, c: &'a i32, d: &'a i32) -> &'a i32 {
    let mut r = a;
    let mut counter = 0;

    loop {
        loop {
            if counter % 2 == 0 {
                r = b;
            } else {
                r = c;
            }

            if random_test() {
                break;
            }
            counter += 1;
        }

        r = d; // Outer loop override
        if random_test() {
            break;
        }
        counter += 1;
    }
    r
}

/// Expected alias analysis result: (0,1)
fn case_72<'a>(x: &'a i32, y: &'a i32) -> &'a i32 {
    let mut r = x;
    let mut flag1 = true;
    let mut flag2 = false;

    loop {
        if flag1 {
            r = x;
        }

        if flag2 {
            // If tracking is precise, we know when flag2=true, flag1 might be false
            // But let's create a strictly impossible state
            if flag1 {
                r = y; // UNREACHABLE assuming logic holds
            }
        }

        // Toggle logic
        if flag1 {
            flag1 = false;
            flag2 = true;
        } else {
            flag1 = true;
            flag2 = false;
        }

        if random_test() {
            break;
        }
    }
    r
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_73<'a>(x: &'a i32, y: &'a i32, z: &'a i32, s: Selector_test2) -> &'a i32 {
    let mut r = x;
    let mut carrier = z; // Carries z to next iter

    loop {
        // Outer logic
        let mut local = match s {
            Selector_test2::First => x,
            Selector_test2::Second => y,
            _ => carrier, // Reachable if s is Third/Fourth OR via logic drift
        };

        loop {
            // Inner logic: depends on s
            r = match s {
                Selector_test2::First => local,  // x
                Selector_test2::Second => local, // y
                _ => z,
            };

            if random_test() {
                break;
            }

            // Mutation
            local = carrier;
        }

        // Loop carried mutation
        if let Selector_test2::First = s {
            carrier = y; // Changes carrier for next outer loop
        }

        if random_test() {
            break;
        }
    }
    r
}

/// Expected alias analysis result: (0,1),(0,3),(0,4)
fn case_74<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut ptr = arg6;
    let mode = if random_test() { 1 } else { 2 };
    let mut loop_cnt = 0;

    loop {
        // Branch A: Sets up pointer
        if mode == 1 {
            ptr = arg1;
        } else {
            ptr = arg2;
        }

        // Noise
        if loop_cnt > 5 {
            ptr = arg3;
        }

        // Branch B: Only returns if mode matches, ensuring correlation
        if mode == 1 {
            if random_test() {
                return ptr;
            } // Must be arg1 (or arg3 if deep loop)
        }

        loop_cnt += 1;
        if loop_cnt > 10 {
            break;
        }
    }

    // Fallback
    if mode == 2 {
        ptr
    } else {
        arg4
    }
}

/// Expected alias analysis result: (0,2),(0,3)
fn case_75<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut res = arg1;
    let mut x = 0;

    loop {
        if x < 5 {
            res = arg2;
        } else {
            // Reachable only after x >= 5
            res = arg3;
        }

        if x > 100 {
            res = arg5; // Fake alias
        }

        if random_test() {
            return res;
        }

        x += 1;
        if x == 10 {
            x = 0;
        }
    }
}

/// Expected alias analysis result: (0,3),(0,4)
fn case_76<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
    arg7: &'a i32,
) -> &'a i32 {
    let mut p = arg1;

    'outer: loop {
        p = arg2;

        let mut inner_count = 0;
        'inner: loop {
            if inner_count == 2 {
                p = arg4; // Deep alias
                break 'outer; // Escapes both loops
            }

            if random_test() {
                p = arg3;
                break 'inner; // Goes back to outer, resetting p to arg2 immediately
            }
            inner_count += 1;
        }

        if random_test() {
            return p;
        } // Can return arg2 or arg3
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3),(0,4)
fn case_77<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut p = arg1;
    let mut i = 0;

    loop {
        // Complex calculation for analyzer
        let index = i % 3;

        if index == 0 {
            p = arg2;
        } else if index == 1 {
            p = arg3;
        } else {
            p = arg4;
        }

        if random_test() && i > 5 {
            // If i > 5, we have rotated through 0, 1, 2 multiple times
            return p;
        }
        i += 1;
    }
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_78<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
    arg7: &'a i32,
) -> &'a i32 {
    let mut p = arg1;
    let mut clean = true;

    loop {
        if clean {
            p = arg1;
        } else {
            // Dirty state
            p = arg2;
            if random_test() {
                p = arg3;
            }
        }

        if random_test() {
            // If clean is true here, we return arg1.
            // If clean is false, we return arg2 or arg3.
            return p;
        }

        // Toggle state logic
        if clean {
            clean = false;
        } else {
            // Sometimes reset
            if random_test() {
                clean = true;
            }
        }
    }
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_79<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
    arg7: &'a i32,
    arg8: &'a i32,
) -> &'a i32 {
    let mut p = arg1;
    let mut counter = 0;

    while counter < 10 {
        let mut temp = arg3;
        if counter > 5 {
            temp = arg2; // Late binding
        }

        // This makes p alias arg3 (early) or arg2 (late)
        if random_test() {
            p = temp;
        }

        // Distractor
        if counter == 99 {
            p = arg8;
        }

        counter += 1;
    }

    p
}

/// Expected alias analysis result: (0,2),(0,3),(0,4)
fn case_80<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut selector = 0;
    let mut p = arg1;

    loop {
        // Selector evolves: 0 -> 1 -> 3 -> 6
        selector += 1;

        if selector == 1 {
            p = arg2;
        } else if selector == 2 {
            p = arg3;
        } else if selector >= 3 {
            p = arg4;
            break;
        }

        // If we break randomly before selector >= 3
        if random_test() {
            return p;
        }
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case_81<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut res = arg1;

    'block: loop {
        res = arg2;
        if random_test() {
            // If we break here, res is arg2
            break 'block;
        }

        // If we continue here, we overwrite res
        res = arg3;

        if random_test() {
            // Fake path
            if false {
                res = arg6;
            }
            return res; // Returns arg3
        }
    }
    // Can reach here with arg2
    res
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_82<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
) -> &'a i32 {
    let mut p_a = arg1;
    let mut p_b = arg2;
    let mut i = 0;

    loop {
        // Swap p_a and p_b
        let temp = p_a;
        p_a = p_b;
        p_b = temp;

        // Inject arg3 into the mix only on 3rd iteration
        if i == 2 {
            p_a = arg3;
        }

        if random_test() {
            return p_a;
        }
        i += 1;
    }
}

/// Expected alias analysis result: (0,1),(0,3)
fn case_83<'a>(
    arg1: &'a i32,
    arg2: &'a i32,
    arg3: &'a i32,
    arg4: &'a i32,
    arg5: &'a i32,
    arg6: &'a i32,
    selector: bool,
) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;

    loop {
        if selector {
            p = q; // p becomes arg2
        } else {
            q = p; // q becomes arg1
        }

        // If selector is true, p aliases arg2.
        // If selector is false, p stays arg1 (q changes, but p doesn't point to q).

        if random_test() {
            // Complex injection
            if selector {
                // If selector true, p is arg2.
                p = arg3;
            }
            return p;
        }
    }
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_84<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random_test() {
            p = arg2;
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,3)
fn case_85<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    if random_test() {
        loop {
            p = arg2;
            if random_test() {
                p = arg3;
                break;
            }
        }
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case_86<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    // SCC 1
    loop {
        if random_test() {
            p = arg2;
            break;
        }
    }
    // SCC 2
    loop {
        if random_test() {
            p = arg3;
            break;
        }
        if random_test() {
            break;
        } // Might preserve arg2 from SCC 1
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case_87<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        p = arg2;
        loop {
            // Inner loop logic
            if random_test() {
                break;
            }
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case_88<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random_test() {
            return arg2; // Direct alias to 2
        }
        p = arg3;
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,4)
fn case_89<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        loop {
            p = arg2;
            loop {
                if random_test() {
                    p = arg3;
                }
                if random_test() {
                    break;
                }
            }
            if random_test() {
                p = arg4;
                break;
            }
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_90<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random_test() {
            p = arg2;
            // "Break" logic
            loop {
                if random_test() {
                    return arg3;
                } // Exit 1
                if random_test() {
                    break;
                } // Exit 2 (to outer)
            }
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_91<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random_test() {
            p = arg2;
            continue; // Skips the break check
        }
        break;
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case_92<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        loop {
            loop {
                loop {
                    p = arg2;
                    if random_test() {
                        break;
                    }
                }
                if random_test() {
                    break;
                }
            }
            if random_test() {
                break;
            }
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case_93<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        loop {
            if random_test() {
                break;
            }
        }
        p = arg2;
        if random_test() {
            break;
        }
    }
    loop {
        loop {
            if random_test() {
                break;
            }
        }
        if random_test() {
            p = arg3;
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,3)
fn case_94<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'outer: loop {
        p = arg2;
        loop {
            if random_test() {
                p = arg3;
                break 'outer; // Bypasses outer loop condition
            }
            if random_test() {
                break;
            }
        }
    }
    p
}

/// Expected alias analysis result: (0,3),(0,4)
fn case_95<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'top: loop {
        p = arg2;
        loop {
            loop {
                if random_test() {
                    p = arg3;
                    break 'top;
                }
                if random_test() {
                    p = arg4;
                    break; // Regular break to middle loop
                }
            }
            break; // Break middle loop
        }
        break; // Break top loop
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_96<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'block: loop {
        if random_test() {
            p = arg2;
            break 'block;
        }
        if random_test() {
            // "Goto" start
            continue 'block;
        }
        break;
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case_97<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        match random_test() {
            true => {
                p = arg2;
                break;
            }
            false => {
                p = arg3;
            } // continues
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,3),(0,4)
fn case_98<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;

    // Left Wing
    loop {
        if random_test() {
            p = arg3;
            break;
        }
    }
    // Right Wing
    loop {
        if random_test() {
            q = arg4;
            break;
        }
    }

    // Merge
    if random_test() {
        p
    } else {
        q
    }
}

/// Expected alias analysis result: (0,2),(0,3)
fn case_99<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        // Simulating integer match with randomness
        let choice = if random_test() { 0 } else { 1 };
        match choice {
            0 => p = arg2,
            1 => p = arg3,
            _ => p = arg4,
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_100<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;
    loop {
        if random_test() {
            let temp = p;
            p = q;
            q = temp;
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_101<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random_test() {
            p = arg2;
        } else if random_test() {
            p = arg3;
        } else {
            // keep arg1
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1)
fn case_102<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if false {
            // Statically dead, but topologically exists
            p = arg2;
        }
        break;
    }
    p
}

/// Expected alias analysis result: (0,4)
fn case_103<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        loop {
            match random_test() {
                true => p = arg2,
                false => p = arg3,
            }
            if random_test() {
                break;
            }
        }
        if random_test() {
            p = arg4;
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,5)
fn case_104<'a>(a: &'a i32, b: &'a i32, c: &'a i32, d: &'a i32, e: &'a i32) -> &'a i32 {
    let mut p = a;
    loop {
        // Noise loops
        loop {
            if random_test() {
                break;
            }
        }

        // Actual assignment
        if random_test() {
            p = e;
        }

        break;
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3),(0,4),(0,5)
fn case_105<'a>(a: &'a i32, b: &'a i32, c: &'a i32, d: &'a i32, e: &'a i32) -> &'a i32 {
    let mut p = a;
    loop {
        if random_test() {
            p = b;
        }
        if random_test() {
            p = c;
        }
        if random_test() {
            p = d;
        }
        if random_test() {
            p = e;
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2),(0,3),(0,4)
fn case_106<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg3;

    loop {
        if random_test() {
            p = arg2;
        }
        if random_test() {
            q = arg4;
        }
        if random_test() {
            break;
        }
    }

    if random_test() {
        p
    } else {
        q
    }
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
fn case_107<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;
    let mut r = arg3;

    loop {
        if random_test() {
            p = q;
        } else {
            q = r;
        }
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case_108<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'outer: loop {
        p = arg2;
        loop {
            if random_test() {
                p = arg3;
                continue 'outer; // Resets execution to top of outer
            }
            break;
        }
        break; // Reached only if inner loop breaks normally
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case_109<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    if random_test() {
        // Path A
        p = arg2;
    } else {
        // Path B
        p = arg3;
    }
    // Shared Loop
    loop {
        if random_test() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_110<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        p = arg2;
        if random_test() {
            p = arg1; // Reset
            break;
        }
        if random_test() {
            break;
        } // Exit with arg2
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3)
fn case_111<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        // Top Loop
        if random_test() {
            p = arg2;
            break;
        }
    }

    match random_test() {
        true => {
            loop {
                // Bottom Loop
                if random_test() {
                    p = arg3;
                    break;
                }
            }
        }
        false => {}
    }
    p
}

/// Expected alias analysis result: (0,2),(0,3),(0,4)
fn case_112<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'outer: loop {
        match random_test() {
            true => loop {
                if random_test() {
                    p = arg2;
                    break 'outer;
                }
                loop {
                    if random_test() {
                        p = arg3;
                        break;
                    }
                }
                if random_test() {
                    break;
                }
            },
            false => {
                p = arg4;
            }
        }
        break;
    }
    p
}