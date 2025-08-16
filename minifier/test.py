from parser import OpenAPIParser
from analyzer import DependencyAnalyzer
from extractor import SpecExtractor, ExtractorConfig
from validator import SpecValidator

# 1) Load
parser = OpenAPIParser.load_spec("../examples/complex-spec.yaml")   # returns OpenAPIParser :contentReference[oaicite:3]{index=3}

# 2) Analyze (choose operations by your selector first; here we hardcode one)
selected = [("/projects/{projectId}/issues", "post")]
keep = DependencyAnalyzer().analyze(parser, selected)
print("====after analyzer===")
print(keep)

# 3) Extract
cfg = ExtractorConfig(
    keep_first_server=True,
    include_descriptions=False,
    include_examples=False,
    drop_vendor_extensions=True,
    keep_only_used_media_types=True,
    hoist_inline_parameters=True,
    hoist_inline_responses=True,
    hoist_inline_request_bodies=True,  # ignored for Swagger 2.0
)
extractor = SpecExtractor(cfg)
minimal_doc = extractor.build_minimal(parser, keep)
print(minimal_doc)

# 4) Validate
validator = SpecValidator(strict=True)
print(validator.validate(parser))
validation_errors = validator.validate(OpenAPIParser(minimal_doc))  # validator expects OpenAPIParser :contentReference[oaicite:4]{index=4}
if validation_errors:
    print("❌ Errors:\n - " + "\n - ".join(validation_errors))
else:
    print("✅ Minified spec is valid.")
