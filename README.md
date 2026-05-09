# AI Works

Miscellaneous AI experiments, reusable prompts, and skill packages.

## Repository Structure

### skills/
Collection of reusable skills for specific workflows.

- `README.md`: Explains what skills are and lists available skill categories.
- `Claude_Code_Top_Skills.md`: Some most useful skills (use with Claude Code or others) 
- `manager/performance-management-design/SKILL.md`: Skill definition for generating role-based SMART performance goals and KPIs from category and role inputs.
- `manager/performance-management-design/references/`: Supporting reference material for the performance-management skill.
- `manager/performance-management-design/scripts/generate_performance_goals.py`: Python CLI script that reads Excel inputs, calls Claude (Anthropic or Anthropic Foundry), and exports goal/KPI output to Excel.
- `manager/performance-management-design/scripts/requirements.txt`: Python dependencies for the goal-generation script.

### talktoprompt/
Voice-to-prompt utility and notes.

- `README.md`: Describes the browser-based tool that turns spoken input into structured prompts.
- `talktoprompt.html`: Standalone HTML page for speech-to-prompt formatting (designed for Azure OpenAI by default, but adaptable).

### useful_prompts/
Prompt templates for common professional tasks.

- `README.md`: High-level folder entry point.
- `Anytime_Feedback.md`: Template to generate professional peer feedback across strengths, development areas, and general comments.
- `Company_Analysis.md`: Two-stage investment workflow prompts for business-model analysis and momentum-based portfolio shortlisting, plus a generic analysis variant.
- `Data_to_Story.md`: Prompt sequence for dataset discovery, story ideation, analysis, visualization, and web-ready storytelling output.
- `Education.md`: Prompt for generating CBSE Class 9 Science exam papers with reflection and quality-check steps.
- `Market_Analysis.md`: Prompt flow for startup market research, competitor review, Blue Ocean positioning, and market sizing.
- `Tune_Resume.md`: ATS-focused resume/profile tuning prompts (including model-specific templates).

## Notes

- Most files in this repo are prompt templates and skill instructions.
- Scripted automation currently exists under the performance-management skill.



