# Open Source AI Toolkit

Practical, beginner-friendly tools and resources for building AI-powered applications.

## First utility: PromptCheck

PromptCheck is a small, dependency-free Python CLI that checks prompt size and flags a few recognizable credential formats before you send text to an AI API.

### Requirements
- Python 3.10+
- No third-party packages

### Run
```bash
python promptcheck.py prompt.txt
cat prompt.txt | python promptcheck.py
python promptcheck.py --text "Explain gradient descent simply"
python promptcheck.py --json prompt.txt
python -m unittest discover -s tests -v
```

### Checks
- Character and word counts
- Rough token estimate (characters divided by four, rounded up)
- Empty input
- A few possible secret patterns

**Important:** The token estimate is not model-specific or exact. Secret matching is heuristic, can produce false positives, and cannot guarantee a prompt is safe. Review findings locally.

### Privacy
The tool processes input locally, makes no network requests, and does not store prompt text. Avoid passing real secrets in command-line arguments because shell history may retain them.

## Contributing
Contributions are welcome. Please open an issue describing the problem or proposal. For pull requests:
1. Explain the use case and expected behavior.
2. Include or update tests.
3. Keep dependencies minimal.
4. Never commit API keys, credentials, or private prompts.

## Roadmap
- Add more test cases and CI
- Add a configurable token-estimation backend only when its limits and dependencies are clear
- Collect beginner-friendly, reviewed examples

## License
MIT. See [LICENSE](LICENSE).
