# Example usage in README.md:
"""

```
from nexus_sdk import HackathonNexusAPI

api = HackathonNexusAPI(api_key="your_gemini_api_key_here")

# Generate questions
files = ["path/to/file1.pdf", "path/to/file2.jpg"]
result = api.generate_questions(files, num_questions=5, difficulty="medium")
print(result)

# Validate answer
validation = api.check_answer(
    question="What is the capital of France?",
    correct_answer="Paris",
    user_answer="London"
)
print(validation)
```

This allows for fine-grained error handling in your applications.
"""

## Install with:
```
pip install nexus-sdk3
```