# What I Unlearned — Hiring Stall Alerter

Before this challenge, much of my independent automation work used visual platforms such as n8n, Make, and Zapier. I was comfortable mapping inputs, conditions, integrations, and outputs, but I had not built a standalone Python application. My first instinct was to compare AI coding tools and wonder whether I needed Claude Code or a stronger programming background before I could start.

**The first assumption I had to let go of was that I needed to know the language before I could attempt the tool.** I used ChatGPT to propose the application structure, generate Python and Streamlit code, and explain how to run it. That let me move from a business objective to a working local application without claiming to be an experienced Python developer.

**The second assumption was that a working screen meant the job was finished.** When the dashboard showed the expected candidate counts, I still needed to test the threshold, search, and export. Later review identified a potential spreadsheet formula interpretation risk in exported CSV values. The tool needed an export-specific safeguard and regression tests. I learned that AI-generated code requires the same scrutiny as any other software.

**The third assumption was that AI-first necessarily meant putting an AI model inside the finished application.** This tool deliberately has no runtime LLM call. ChatGPT was used for design, code generation, debugging, and revisions; Python applies deterministic date calculations and follow-up rules. For this problem, that makes the output easier to reproduce and explain.

I also began to understand the importance of a continuous integration workflow. GitHub Actions exposed failures when a verification script had not yet been committed. Those results taught me to examine the actual failed step instead of treating every red run as a failure of the core application. After the repository was complete, the tests and reference checks passed.

**What changed in how I work:** I can use AI to explore unfamiliar software technologies, but I should define the problem clearly, test important behavior myself, inspect errors, and keep a record of what was actually verified. I do not need to claim I personally wrote every line for that learning to be meaningful.

**What I still need to build:** independent fluency reading and changing Python code, manual Excel save/reopen validation, real deployment experience, and eventually secure integrations with a persistent hiring database or ATS. This project is a starting point for AI-assisted engineering, not proof that I have already mastered production software development.
