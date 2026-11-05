import Lake
open Lake DSL

package ophStage4

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @
  "d3739f06187591e81887886ca767b6a2dc1416ea"

@[default_target]
lean_lib OphStage4 where
  srcDir := "."
  roots := #[`OphStage4, `OphStage4Audit]
