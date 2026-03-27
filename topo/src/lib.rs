// Helper function to simulate non-deterministic control flow
fn random() -> bool {
    true // Implementation detail irrelevant for static analysis
}

/// Expected alias analysis result: (0,1),(0,2),(0,3)
pub fn case_1<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p3;
    loop {
        if random() {
            res = p1;
            loop {
                if random() {
                    res = p2;
                }
                if random() {
                    break;
                }
            }
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result: (0,1),(0,3),(1,3)
pub fn case_2<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p2;
    loop {
        // Outer loop
        res = *p1;
        loop {
            // Inner loop: Input-Input aliasing
            if random() {
                *p1 = p3; // Arg1 now aliases Arg3
                res = p3;
            }
            if random() {
                break;
            }
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_3<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, _p4: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        loop {
            loop {
                if random() {
                    res = p2;
                }
                if random() {
                    break;
                }
            }
            if random() {
                res = p3;
            }
            if random() {
                break;
            }
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2)
pub fn case_4<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if random() {
            // Guarded Inner Loop
            let mut inner_ptr = p3;
            loop {
                inner_ptr = p2;
                if random() {
                    break;
                }
            }
            res = inner_ptr;
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3), (0, 4)
pub fn case_5<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        let mut temp = res;
        loop {
            if random() {
                temp = p2;
            } else {
                temp = p3;
            }
            if random() {
                break;
            }
        }
        res = temp; // Propagate inner alias to outer
        if random() {
            res = p4;
        }
        if random() {
            break;
        }
    }
}

/// Expected alias analysis result:(0,5),(1,2),(1,3),(0,2),(0,3)
pub fn case_6<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, p5: &'a i32) -> &'a i32 {
    let mut res = p4;
    loop {
        if random() {
            // Inner loop modifies Input p1
            loop {
                if random() {
                    *p1 = p2;
                } else {
                    *p1 = p3;
                }
                if random() {
                    break;
                }
            }
            res = *p1;
        } else {
            res = p5;
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0,2),(0,3)
pub fn case_7<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p1;
    'outer: loop {
        loop {
            if random() {
                res = p2;
                break 'outer; // Jump out of both
            }
            if random() {
                res = p3; // Local to inner, then might break inner
                break;
            }
        }
        // If we broke inner but not outer
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_8<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p3;
    loop {
        if random() {
            res = p1;
        }
        loop {
            // This inner loop might not affect res if we don't assign
            if random() {
                res = p2;
            }
            if random() {
                break;
            }
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result: (0, 3), (1, 3)
pub fn case_9<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p2;
    loop {
        loop {
            loop {
                // Deepest level
                *p1 = p3; // Arg1 aliases Arg3
                res = *p1;
                if random() {
                    break;
                }
            }
            if random() {
                break;
            }
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2)
pub fn case_10<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p3;
    loop {
        if random() {
            return p1; // Early exit 1
        }
        if random() {
            res = p2;
            break; // Exit slice 2
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_11<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if random() {
            res = p2;
            continue; // Go back to start, res is p2
        }
        if random() {
            res = p3;
            break;
        }
        // Fallthrough
        break;
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 4)
pub fn case_12<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32) -> &'a i32 {
    loop {
        if random() {
            return p1;
        }
        if random() {
            if random() {
                return p2;
            }
            // Modify local state and continue
            let _unused = p3;
            continue;
        }
        if random() {
            return p4;
        }
    }
}

/// Expected alias analysis result:(0, 2), (0, 3), (1, 2)
pub fn case_13<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    loop {
        if random() {
            *p1 = p2; // Alias change
            return *p1; // Returns p2 (via p1)
        }
        if random() {
            return p3;
        }
    }
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_14<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if random() {
            res = p2;
            break;
        }
        if random() {
            return p3;
        }
        // This path continues loop
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_15<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if random() {
            res = p2;
            break;
        }
        if random() {
            res = p3;
            break;
        }
        if random() {
            res = p4; // Updates but doesn't break immediately
        }
        // Implicit continue
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 3)
pub fn case_16<'a>(p1: &'a i32, _p2: &'a i32, p3: &'a i32) -> &'a i32 {
    loop {
        if random() {
            return p1;
        } else {
            return p3;
        }
    }
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_17<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        res = p2;
        if random() {
            break;
        }
        res = p3;
        if random() {
            return res;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_18<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if random() {
            res = p2;
            // No break, loops back with res=p2
        } else {
            return res; // Can be p1 or p2
        }
        if random() {
            return p3;
        }
    }
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3)
pub fn case_19<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p1;
    // Sibling A
    loop {
        if random() {
            res = p2;
        }
        if random() {
            break;
        }
    }
    // Sibling B
    loop {
        // Input to B comes from Output of A
        if random() {
            res = p3;
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(1,2),(0,1),(0,2),(0,3)
pub fn case_20<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    // Sibling A
    loop {
        if random() {
            *p1 = p2; // Arg1 aliases Arg2
        }
        if random() {
            break;
        }
    }

    let mut res = p3;
    // Sibling B
    loop {
        if random() {
            res = *p1; // Reads modified p1 (could be original or p2)
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4)
pub fn case_21<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32) -> &'a i32 {
    let mut res = p1;
    // Loop 1
    loop {
        if random() {
            res = p2;
        }
        if random() {
            break;
        }
    }
    // Loop 2
    loop {
        if random() {
            res = p3;
        }
        if random() {
            break;
        }
    }
    // Loop 3 (Sibling)
    loop {
        if random() {
            res = p4;
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_22<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p1;
    // Loop A
    loop {
        res = p2;
        if random() {
            break;
        }
    }

    if random() {
        // Loop B
        loop {
            res = p3;
            if random() {
                break;
            }
        }
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_23<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut temp1 = p1;
    // Loop A
    loop {
        temp1 = p2;
        if random() {
            break;
        }
    }

    let mut temp2 = p3;
    // Loop B
    loop {
        // Doesn't touch temp1
        if random() {
            break;
        }
    }

    // Merge after loops
    if random() {
        temp1
    } else {
        temp2
    }
}

/// Expected alias analysis result:(0, 3), (0, 4)
pub fn case_24<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32) -> &'a i32 {
    let mut res = p1;
    // Loop A
    loop {
        if random() {
            res = p2;
        }
        if random() {
            break;
        }
    }
    // Loop B
    loop {
        // Assigns from p3 or p4, overwriting A's result
        if random() {
            res = p3;
        } else {
            res = p4;
        }

        if random() {
            break;
        }
    }

    res
}

/// Expected alias analysis result:(0, 2), (0, 3), (0, 4), (0, 5)
pub fn case_25<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32, p5: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        // Simulating match statement with high fan-out
        if random() {
            res = p2;
        } else if random() {
            res = p3;
        } else if random() {
            res = p4;
        } else {
            res = p5;
        }

        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3), (0, 4), (1, 3)
pub fn case_26<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32) -> &'a i32 {
    let mut res = p4;
    loop {
        if random() {
            res = p2;
        } else if random() {
            *p1 = p3; // Branch 2 creates input alias
            res = *p1;
        } else {
            res = p4;
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (0, 4)
pub fn case_27<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if random() {
            if random() {
                res = p2;
            } else {
                res = p3;
            }
        } else {
            if random() {
                res = p4;
            }
            // else keep p1
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result:(0, 2), (0, 3)
pub fn case_28<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if random() {
            res = p2;
        } else if random() {
            res = p2; // Aliases p2 again
        } else if random() {
            res = p2; // Aliases p2 again
        } else {
            res = p3;
        }
        if random() {
            break;
        }
    }
    // p4 is never aliased
    res
}

/// Expected alias analysis result: (0, 3), (0, 4)
pub fn case_29<'a>(p1: &'a i32, p2: &'a i32, p3: &'a i32, p4: &'a i32) -> &'a i32 {
    let mut res = p1;
    loop {
        if random() {
            res = p2;
        } else if random() {
            return p3; // Exit slice
        } else if random() {
            res = p4;
            break; // Break slice
        }
        // Fallthrough keeps res (p1 or p2)
    }
    res
}

/// Expected alias analysis result:(0, 1), (0, 2), (0, 3), (1, 3)
pub fn case_30<'a>(p1: &mut &'a i32, p2: &'a i32, p3: &'a i32) -> &'a i32 {
    let mut res = p2;
    loop {
        if random() {
            res = *p1; // Reads original p1 target
        } else if random() {
            *p1 = p3; // Modifies p1
            res = p2;
        } else {
            res = p3;
        }
        if random() {
            break;
        }
    }
    res
}

/// Expected alias analysis result: (0,1),(0,2)
pub fn case_31<'a>(x: &'a i32, y: &'a i32) -> &'a i32 {
    let mut p = x;
    loop {
        if random() {
            break;
        } // Can return x (Iter 0) or y (Iter 1+)
        p = y;
    }
    p
}

/// Expected alias analysis result: (0,2)
pub fn case_32<'a>(x: &'a i32, y: &'a i32, z: &'a i32) -> &'a i32 {
    let mut p = x;
    loop {
        p = y;
        loop {
            // Noise: local pointer manipulation that shouldn't escape
            let mut _q = z;
            if random() {
                break;
            }
        }
        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result: (0,1),(0,2)
pub fn case_33<'a>(x: &'a i32, y: &'a i32) -> &'a i32 {
    let mut p = x;

    // Loop 1: Unconditionally sets p to y eventually
    while random() {
        p = y;
        break;
    }

    // Loop 2: Does not mutate p
    while random() {
        if random() {
            return p;
        }
    }

    p
}

/// Expected alias analysis result: (0,3)
pub fn case_34<'a>(x: &'a i32, y: &'a i32, z: &'a i32) -> &'a i32 {
    let mut p = x;
    loop {
        p = y; // Outer sets to y
        loop {
            loop {
                p = z; // Inner sets to z
                break; // Breaks depth 3
            }
            break; // Breaks depth 2
        }
        // p is now z
        break; // Breaks depth 1
    }
    p
}

/// Expected alias analysis result: (0,2)
fn case_35<'a>(v1: &'a i32, v2: &'a i32) -> &'a i32 {
    let mut r = v1;
    loop {
        loop {
            loop {
                loop {
                    loop {
                        loop {
                            r = v2;
                            if random() {
                                break;
                            }
                        }
                        if random() {
                            break;
                        }
                    }
                    if random() {
                        break;
                    }
                }
                if random() {
                    break;
                }
            }
            if random() {
                break;
            }
        }
        if random() {
            break;
        }
    }
    r
}

/// Expected alias analysis result: (0,1)
fn case_36<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;
    loop {
        q = arg3; // q is modified
        if random() {
            break;
        }
    }
    p // p should still only be arg1
}

/// Expected alias analysis result: (0,1),(0,2)
fn case_37<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        // No iteration delay
        if random() {
            p = arg2;
        }

        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,3)
fn case_38<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;

    if random() {
        loop {
            if random() {
                p = arg2;
            }

            if random() {
                p = arg3;
                break;
            }
        }
    }
    p
}

/// Expected alias analysis result:(0,2),(0,3)
fn case_39<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;

    // SCC 1
    loop {
        if random() {
            p = arg2;
            break;
        }
    }

    // SCC 2
    loop {
        // Previously depended on flag from SCC 1
        if random() {
            p = arg3;
            break;
        }
        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2)
fn case_40<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random() {
            p = arg2;
        }

        loop {
            if random() {
                break;
            }
        }
    }
    p
}

/// Expected alias analysis result:(0,2),(0,3)
fn case_41<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random() {
            return arg2;
        }
        p = arg3;

        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,4)
fn case_42<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        loop {
            p = arg2;
            loop {
                if random() {
                    p = arg3;
                    break;
                }
            }
            if random() {
                p = arg4;
                break;
            }
        }
        break;
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2),(0,3)
fn case_43<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random() {
            p = arg2;
            loop {
                if random() {
                    return arg3;
                }
                if random() {
                    break;
                }
            }
        }
        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2)
fn case_44<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random() {
            p = arg2;
            continue;
        }
        break;
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2)
fn case_45<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        loop {
            loop {
                loop {
                    if random() {
                        p = arg2;
                    }
                    if random() {
                        break;
                    }
                }
                if random() {
                    break;
                }
            }
            if random() {
                break;
            }
        }
        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,3)
fn case_46<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;

    // Loop 1
    loop {
        p = arg2;
        break;
    }

    // Loop 2
    loop {
        p = arg3;
        break;
    }
    p
}

/// Expected alias analysis result:(0,3)
fn case_47<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'outer: loop {
        p = arg2;
        loop {
            if random() {
                p = arg3;
                break 'outer;
            }
            if random() {
                break;
            }
        }
    }
    p
}

/// Expected alias analysis result:(0,3)
fn case_48<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'top: loop {
        p = arg2;
        loop {
            loop {
                if random() {
                    p = arg3;
                    break 'top;
                }
                if random() {
                    p = arg4;
                    break;
                }
            }
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2)
fn case_49<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'block: loop {
        if random() {
            p = arg2;
            break 'block;
        }
        if random() {
            continue 'block;
        }
        break;
    }
    p
}

/// Expected alias analysis result:(0,2),(0,3)
fn case_50<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random() {
            p = arg2;
            break;
        } else {
            p = arg3;
        }

        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,3),(0,4)
fn case_51<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;

    // Left Wing
    loop {
        if random() {
            p = arg3;
            break;
        }
    }

    // Right Wing
    loop {
        if random() {
            q = arg4;
            break;
        }
    }

    // Merge
    if random() {
        p
    } else {
        q
    }
}

/// Expected alias analysis result:(0,2),(0,3),(0,4)
fn case_52<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random() {
            p = arg2;
        } else if random() {
            p = arg3;
        } else {
            p = arg4;
        }

        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2)
fn case_53<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;
    loop {
        if random() {
            let temp = p;
            p = q;
            q = temp;
        }

        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2),(0,3)
fn case_54<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random() {
            p = arg2;
        } else if random() {
            p = arg3;
        } else {
            // keep arg1
        }

        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2)
fn case_55<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        if random() {
            p = arg2;
        }

        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,4)
fn case_56<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        loop {
            if random() {
                p = arg2;
            } else {
                p = arg3;
            }
            if random() {
                break;
            }
        }

        if random() {
            p = arg4;
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,5)
fn case_57<'a>(a: &'a i32, b: &'a i32, c: &'a i32, d: &'a i32, e: &'a i32) -> &'a i32 {
    let mut p = a;
    loop {
        loop {
            if random() {
                break;
            }
        }

        if random() {
            p = e;
        }

        break;
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2),(0,3),(0,4),(0,5)
fn case_58<'a>(a: &'a i32, b: &'a i32, c: &'a i32, d: &'a i32, e: &'a i32) -> &'a i32 {
    let mut p = a;
    loop {
        if random() {
            p = b;
        }
        if random() {
            p = c;
        }
        if random() {
            p = d;
        }
        if random() {
            p = e;
        }

        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2),(0,3),(0,4)
fn case_59<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg3;

    loop {
        if random() {
            p = arg2;
        } else {
            q = arg4;
        }

        if random() {
            break;
        }
    }

    if random() {
        p
    } else {
        q
    }
}

/// Expected alias analysis result:(0,1),(0,2),(0,3)
fn case_60<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    let mut q = arg2;
    let mut r = arg3;

    loop {
        if random() {
            p = q;
        }

        if random() {
            q = r;
        }

        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,2)
fn case_61<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'outer: loop {
        p = arg2;
        loop {
            if random() {
                p = arg3;
                continue 'outer;
            }
            break;
        }
        break;
    }
    p
}

/// Expected alias analysis result:(0,2),(0,3)
fn case_62<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;

    if random() {
        p = arg2;
    } else {
        p = arg3;
    }

    loop {
        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2)
fn case_63<'a>(arg1: &'a i32, arg2: &'a i32) -> &'a i32 {
    let mut p = arg1;
    loop {
        p = arg2;
        if random() {
            p = arg1;
            break;
        }
        if random() {
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,3)
fn case_64<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32) -> &'a i32 {
    let mut p = arg1;

    loop {
        if random() {
            p = arg2;
            break;
        }
    }

    loop {
        if random() {
            p = arg3;
            break;
        }
    }
    p
}

/// Expected alias analysis result:(0,1),(0,2),(0,3),(0,4)
fn case_65<'a>(arg1: &'a i32, arg2: &'a i32, arg3: &'a i32, arg4: &'a i32) -> &'a i32 {
    let mut p = arg1;
    'outer: loop {
        if random() {
            loop {
                if random() {
                    p = arg2;
                    break 'outer;
                }

                loop {
                    if random() {
                        p = arg3;
                        break;
                    }
                    break;
                }
                if random() {
                    break;
                }
            }
        } else {
            p = arg4;
        }
        break;
    }
    p
}
