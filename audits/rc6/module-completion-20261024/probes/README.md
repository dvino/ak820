# Diagnostic probes

These files retain intermediate compiler/layout and focused linked evidence.
`*-witness.tar.gz` archives are compact subsets, not complete build trees.
They retain emitted/listed code, image/map/memory files and available logs or
reports needed to understand each size or stack failure. Missing final
qualification is deliberate; no probe qualifies the completed source.

The full final development images, raw builds and regression reports are
retained separately after qualification. The JSON files here describe the
exact earlier images named inside them and are not transferred to new images.
