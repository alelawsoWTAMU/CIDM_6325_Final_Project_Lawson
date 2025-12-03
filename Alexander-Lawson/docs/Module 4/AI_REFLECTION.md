# AI Reflection: Module 4 - CBV Refactoring and Architectural Analysis

**Author**: Alexander Lawson  
**Date**: November 20, 2025  
**Module**: 4 - Class-Based Views and Architecture Patterns  
**Word Count**: 587

## Overview

Module 4 challenged me to refactor the blog application from Function-Based Views (FBVs) to Class-Based Views (CBVs) while maintaining 100% feature parity with Module 3's authentication, HTMX search, comments, and form validation. Working with GitHub Copilot as my AI pair programmer, I discovered both the power and limitations of AI-assisted architectural refactoring. This reflection documents my experience with prompt engineering, decision-making processes, and the balance between AI suggestions and human judgment.

## Effective Prompts and Strategies

The most successful prompts were **specific and contextual**, providing clear requirements and existing code structure. For example:

> "Convert the post_update view to PostUpdateView using UpdateView with LoginRequiredMixin and UserPassesTestMixin. The test_func should check if request.user equals post.author or request.user.is_superuser."

This prompt worked because it specified: (1) the target class name, (2) required mixins in correct order, (3) the exact logic for authorization. Copilot generated the correct implementation in one attempt, understanding both the Django pattern and the business requirement.

In contrast, vague prompts like "make my views better" or "add permissions" produced generic suggestions that didn't account for our specific superuser bypass requirement. **The lesson: AI excels at pattern implementation when given precise constraints.**

Another effective strategy was **asking for comparisons before making changes**:

> "Show me the before and after code if I convert post_create to a CBV using CreateView."

This allowed me to evaluate the tradeoffs (fewer lines, declarative mixins, but less explicit flow control) before committing to the refactoring. The AI provided side-by-side comparisons that highlighted both benefits (37% code reduction) and costs (deeper call stack for debugging).

## Architectural Decision Support

When documenting the FBV vs CBV tradeoffs for Part A, I prompted:

> "Create a decision matrix comparing FBV and CBV approaches across readability, maintainability, reusability, testability, performance, and learning curve dimensions."

Copilot generated a comprehensive table with nuanced assessments—not just "CBV is better," but context-dependent evaluations like "FBV wins for readability due to explicit logic flow" while "CBV wins for maintainability through DRY principles." This helped me understand that **architectural decisions are multidimensional**, and the "right" answer depends on team experience, project complexity, and maintenance priorities.

However, the AI initially suggested converting the `search_posts` view to a `FilterView` CBV. When I tested this, the HTMX partial rendering broke because `FilterView` expects full-page templates. I had to override this decision and keep `search_posts` as an FBV, demonstrating that **AI recommendations need validation against actual requirements**. The hybrid approach (CBVs for CRUD, FBV for custom logic) emerged from this human-AI collaboration.

## Documentation and Critique Challenges

For the architectural critique tasks (Parts B and E), I learned that **AI-generated analysis requires significant human curation**. Prompts like:

> "Critique the TravelMathLite repository for modularity and scalability choices."

Generated structurally sound documents with proper headings and evaluation criteria, but lacked **specific code examples and concrete recommendations**. I had to manually fill in sections with actual repository analysis, turning the AI-generated template into substantive critique.

The most valuable AI contribution here was **providing comprehensive frameworks**—checklists for WCAG compliance, rubrics for code quality, and structured templates for peer review. These saved time on document scaffolding, letting me focus on analytical content.

## Peer Review and Discussion

For Part D responses, I found that **iterative refinement produced better results**:

1. Initial prompt: "Write a response to this discussion post about CBVs."
2. AI output: Generic, surface-level (~120 words)
3. Refinement: "Add specific code examples, discuss mixin ordering, and ask a follow-up question about their test_func implementation."
4. Improved output: Substantive, technical, exceeded 150-word minimum

This taught me that **AI collaboration is iterative**, not one-shot. The first response is often a draft that requires human expertise to add depth, specificity, and authentic engagement.

## Limitations and Manual Interventions

Several tasks required manual intervention:

1. **Complex permission logic**: test_func() with superuser bypass needed custom logic beyond standard patterns
2. **HTMX integration**: AI didn't automatically recognize the need to preserve partial template rendering
3. **Cross-file consistency**: URL pattern updates required manual verification that names matched existing templates
4. **Critical analysis**: Architectural critiques needed domain expertise AI couldn't provide

## Conclusion

Module 4 reinforced that **AI is a powerful accelerator, not a replacement, for software engineering judgment**. Copilot excelled at implementing known patterns (generic CBVs, standard mixins), generating documentation scaffolds, and providing comparison frameworks. However, architectural decisions—like choosing hybrid FBV/CBV approach, evaluating peer code quality, and critiquing scalability choices—required human expertise.

The key to effective AI collaboration is **specificity in prompts, iteration on outputs, and validation of all suggestions against real requirements**. This module transformed my view of AI from "code generator" to "intelligent assistant" that amplifies my capabilities while respecting the irreplaceable role of human architectural thinking.
