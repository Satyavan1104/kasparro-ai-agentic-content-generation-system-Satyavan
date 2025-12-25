# Applied AI Engineer Challenge: Multi-Agent Content Generation System 
Agentic automation system that generates structured product, FAQ, and comparison pages from raw product data using multi-agent workflows, reusable logic blocks, and template-driven JSON outputs.

## Problem Statement
Many existing content generation systems are built as tightly coupled pipelines where data interpretation, content logic, and output formatting are handled within a single workflow. While functional, these designs limit flexibility and make it difficult to reuse logic, introduce new content types, or clearly reason about system behavior.

## Objective 
The objective of this project is to Design and implement a modular agentic automation system that takes a small product dataset and automatically generates structured, machine-readable content pages.  
- multi-agent workflows
- automation graphs
- reusable content logic
- template-based generation
- structured JSON output
- system abstraction & documentation 

---
## Solution Overview

This system implements an agentic pipeline that:

- Parses raw product fields into a normalized internal dictionary
- Generates categorized user questions (designed to support 15+ FAQ entries)
- Generates a fictional competitor product record for comparison
- Assembles page JSON via a custom template engine and reusable content blocks
- Persists final artifacts to `outputs/`
- 
## Scopes & Assumptions

Scope
- Design and implementation of a multi-agent content automation system
- Ingestion of a single structured product dataset as input
- Agent-based parsing, content logic generation, and page assembly
- Generation of Product, FAQ, and Comparison pages
- Output of all generated content in structured JSON format
- Use of reusable content logic blocks and custom templates

Assumptions
- Input data follows a consistent and predefined structure
- No external APIs, databases, or research are used
- All generated content is derived strictly from the provided dataset
- Product comparison is performed against a fictional competit
- The system operates as a batch, single-run pipeline

## System Design 
The system is designed as a **layered, agentic architecture** with explicit data flow and zero hidden global state.

## System Architecture
High-level system architecture illustrating the agentic content generation pipeline, including the orchestrator, autonomous agents, reusable content blocks, template engine, and structured JSON outputs.

![System Architecture](System%20Design/System%20Architecture.jpeg)

### Agents and responsibilities 
The workflow is split into a small set of agents, each with a strict scope:
- **Parsing agent**: normalizes raw input fields into a consistent internal representation.
- **Question generation agent**: produces categorized questions (designed to support 15+ FAQ entries).
- **Competitor generation agent**: creates a fictional “Product B” record for comparison.
- **Content generation agent**: renders structured page JSON using templates + reusable logic blocks.
- **Output agent**: persists JSON artifacts to disk.
This separation makes it easy to replace or extend individual steps without rewriting the pipeline.

--- 

## Orchestration Graph (DAG)
The system runs as a linear pipeline (a simple DAG) showing the execution order and data dependencies between agents, from product data parsing to page generation and output persistence.

![Orchestration Graph](System%20Design/DAG.jpeg)

At runtime, the orchestrator also emits a machine-readable graph artifact (`outputs/graph.json`) describing:
- `nodes`: pipeline steps + agent identity
- `edges`: execution order
- `entry` / `exit`: start/end step IDs

---

## Flowchart
End-to-end flowchart representing the overall content generation process, from input ingestion through content block generation, page rendering, and final JSON output.

![Flowchart](System%20Design/Flow.jpeg)

---

## Sequence Diagram
Sequence diagram depicting runtime interactions between the orchestrator and individual agents, highlighting explicit message passing and coordinated execution.

![Sequence Diagram](System%20Design/Sequence%20Diagram.jpeg)

---

### Output artifacts and expected structure

The pipeline produces:
- **`faq.json`**: includes `faq_items` plus an explicit grouped structure (`faq_by_category`) to make categorization machine-readable.
- **`product_page.json`**: single-product structured page output.
- **`comparison_page.json`**: comparison between Product A and fictional Product B.
- **`graph.json`**: the orchestration graph with `nodes` and `edges`.

## Output
The system generates JSON files in `outputs/`:
- `faq.json`: FAQ page with **15+** categorized Q&As
- `product_page.json`: structured product page JSON
- `comparison_page.json`: structured comparison page JSON
- `graph.json`: machine-readable automation graph (nodes + edges)

## Conclusion
This project successfully delivers a structured, scalable, and efficient system by integrating well-defined data formats, clear system design, and modular components. Through the use of organized JSON files, detailed system architecture, and workflow diagrams, the project ensures smooth data handling, easy maintenance, and flexibility for future enhancements. Overall, the solution demonstrates a practical and reliable approach to building modern, data-driven applications while meeting functional and usability requirements.

