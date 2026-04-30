---
name: spec-forge
description: |
  通过迭代访谈创建详细规格文档（PRD/设计文档）。深度挖掘隐性复杂性和技术权衡。
  当用户要求创建 spec、PRD、设计文档，或需要需求澄清时触发。
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Spec Forge

Transforms high-level requirements into detailed specification documents through iterative interviewing using the `AskUserQuestionTool`. Spec Forge conducts in-depth interviews about technical implementation, UI/UX design, concerns, and tradeoffs—then writes comprehensive markdown specification documents.

## When to Use

Use Spec Forge when:
- User asks to create a spec, PRD, or design document
- User provides a file/instruction and requests detailed interviewing
- Starting planning phase before implementation
- Designing complex features requiring deep analysis

**Critical:** Only use when explicitly asked to create a spec or interview about requirements. Do not use for simple clarification questions or quick implementation tasks.

## Workflow

### 1. Analyze Input First

Before asking any questions, thoroughly read and understand the provided context:
- If user provided a file: Read it completely
- If user provided instructions: Understand the full scope
- Identify what's already clear vs. what needs exploration

### 2. Begin Interviewing

Start with high-level questions, then iteratively drill deeper based on answers. Use **multiple rounds** of questioning—each round should go deeper based on previous responses.

**Interview principles:**

- **Avoid obvious questions** - Don't ask what you can reasonably infer or assume
- **Challenge assumptions** - Explore edge cases, failure modes, what could go wrong
- **Probe for hidden complexity** - Dig into technical implications of stated requirements
- **Explore tradeoffs** - Ask about alternatives and why certain approaches are preferred

**Question examples:**

- Instead of "What should the button do?", ask "What happens if the user clicks while the operation is still in progress?"
- Instead of "Should we use SQL or NoSQL?", ask "This data seems relational—have you considered eventual consistency requirements that might push you toward NoSQL?"
- Instead of "What's the success criteria?", ask "How will you know this is working 6 months from now? What metrics would indicate failure?"

**Continue interviewing** until you have sufficient information to write a comprehensive spec. Use your judgment—when you understand requirements, technical design, tradeoffs, and success criteria, you're ready to proceed.

**Final check before writing:** Present a brief summary of understanding and ask: "I have enough to write the spec. Shall I proceed, or is there more you'd like to add?"

### 3. Write Specification Document

Write the spec to a file and present a summary to the user. Use markdown format with these sections (adapt based on context):

**Standard sections:**
- **Problem & Motivation** - What problem are we solving, for whom, and why now
- **Requirements** - Functional requirements, user stories, acceptance criteria
- **Technical Design** - System architecture, data models, APIs, technology choices
- **Success Criteria** - Success metrics, KPIs, how to measure if it works

**Additional sections as needed:**
- User flows / UX considerations (for UI-heavy features)
- Non-functional requirements (performance, security, scalability)
- Open questions / Decisions pending
- Alternatives considered and why they were rejected
- Implementation phases or milestones

**File location:** Ask user where to save the spec, or suggest a sensible default (e.g., `docs/specs/[feature-name].md` or `SPEC.md`)

**Delivery:** After writing the file, present a brief summary in chat highlighting:
- Problem being solved
- Key technical decisions
- Major tradeoffs discussed
- Any open questions remaining

## Interview Guidelines

### Good Questions vs. Bad Questions

**Bad (obvious):**
- "What should this feature do?"
- "Who are the users?"
- "Should we add error handling?"

**Good (non-obvious):**
- "What happens when two users edit this resource simultaneously?"
- "The requirements mention X—but what about Y edge case?"
- "You chose approach A. Have you considered B? Here's why B might be better..."
- "What's the failure mode if this dependency goes down?"

### Iterative Deep-Dive Pattern

**Round 1 - High-level understanding:**
- Core problem and users
- Main requirements and constraints
- Success vision

**Round 2 - Technical depth:**
- Architecture implications
- Data flows and state management
- Integration points and dependencies
- Performance/security concerns

**Round 3 - Edge cases and tradeoffs:**
- Failure scenarios and error handling
- Scalability considerations
- Alternative approaches and why rejected
- Long-term maintainability

Continue rounds as needed based on complexity.

### When to Stop Interviewing

**Ready to write when you have:**
- Clear problem statement and motivation
- Complete functional requirements
- Coherent technical approach
- Awareness of major tradeoffs and risks
- Defined success criteria
- Understanding of edge cases and failure modes

**If stuck or uncertain:** Ask user focused questions about the specific area that's unclear. Don't guess—ask.

## Output Format Guidelines

### Document Structure

Use clear, hierarchical markdown structure:

```markdown
# [Feature/System] Specification

## Problem & Motivation
[Why are we doing this? What problem does it solve?]

## Requirements
### Functional Requirements
- [Requirement 1]
- [Requirement 2]

### User Stories
- As a [user type], I want [action] so that [benefit]

### Acceptance Criteria
- [Criteria 1]
- [Criteria 2]

## Technical Design
### Architecture
[System overview, components, interactions]

### Data Model
[Entities, relationships, key fields]

### API Endpoints (if applicable)
- [Method] [Path] - [Description]
  - Request: [schema]
  - Response: [schema]

### Technology Choices
- [Technology]: [Justification]

## Success Criteria
- [Metric 1]: [Target/Definition]
- [Metric 2]: [Target/Definition]

## [Additional sections as needed]
```

### Writing Style

- **Use present tense** - "The system validates..." not "The system will validate..."
- **Be specific** - Provide concrete examples, not vague descriptions
- **Include diagrams** - Use ASCII art or mermaid diagrams for architecture/flows when helpful
- **Cite tradeoffs** - Document why certain approaches were chosen over alternatives
- **Think long-term** - Consider maintenance, scalability, and evolution

### Quality Checklist

Before considering the spec complete:
- [ ] Problem statement is clear and motivating
- [ ] Requirements are complete and unambiguous
- [ ] Technical design is coherent and justified
- [ ] Edge cases and failure modes are addressed
- [ ] Success criteria are measurable
- [ ] Tradeoffs and alternatives are documented
- [ ] File is saved to appropriate location
- [ ] Summary presented to user
