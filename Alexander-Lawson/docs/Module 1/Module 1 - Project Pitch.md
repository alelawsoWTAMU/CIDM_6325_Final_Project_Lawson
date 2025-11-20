# Module 1 - Project Pitch

## 🏠 Project Pitch: Home Maintenance Compass

### Problem

New homeowners frequently succumb to a **daunting and reactive approach** to home maintenance. Whether it is because the tasks are “scary” or anxiety-inducing or the new homeowner has no one in their upbringing who mentored them in Homeownership 101, critical tasks like checking the HVAC system, cleaning gutters, or inspecting the roof are often pushed aside until a problem arises. This can lead to **costly and stressful repairs** or inexperienced, foolhardy DIY hacks, which can only exacerbate the situation. Information on when and how to perform these tasks is scattered, unverified, and nonspecific, rarely accounting for a home's specific age, location, or seasonal climate.

The problem is twofold: a **lack of structured, personalized guidance** and a **fragmented ecosystem of reliable, localized or uncommon knowledge.**

Home Maintenance Compass attacks this problem by creating a **personalized, proactive maintenance scheduler** combined with a **curated knowledge base of localized, peer-reviewed tips.** The problem is primarily **logistical** (structuring a maintenance plan that applies to one’s own circumstances), but also **communal** (collecting and curating practical, on-the-ground advice).

---

### Stakeholders

* **First-time Homeowners:** This tool is primarily targeted at homeowners, especially first-time buyers, coming from both the Millennial and Gen Z generations, seeking a structured, proactive maintenance plan, recommendations on service providers in their community or tips for those interested in DIY, but having no one in their immediate social/familial circle they can ask those kinds of questions too.
* **Budget-Conscious Users:** Homeowners who want to extend the life of their systems and avoid expensive, emergency repairs, or who may be interested in DIY solutions to the wide array of challenges posed by owning property. These individuals would be considered “frugal” or looking to get their best “bang-for-their-buck.”
* **Community Contributors:** Experienced homeowners and local contractors who submit tips on common problems, reliable vendors, or seasonal advice. Local contractors/businesses especially would be incentivized to promote their services to potential customers.
* **Property Managers:** Professional property managers/personnel seeking a centralized tool to manage maintenance for multiple properties.
* **Insurance Companies:** Entities interested in promoting preventative maintenance to reduce financial claims related to neglect. This would lower the volume of insurance claims, which means less work, and save the companies both time and money in the long run.

---

### Scope

#### In-scope

* **Personalized Maintenance Schedule:** A user-generated schedule based on key inputs like home age, construction type, climate zone, user competence in a related skillset (electrical, carpentry, automotive, etc.) and major appliance ages. The schedule will trigger reminders for monthly, seasonal, and annual tasks.
* **Maintenance Task Profiles:** Each task (e.g., "Clean Gutters," "Service HVAC", “Drain Water Heater”) will have a dedicated profile detailing a step-by-step guide, required tools, and estimated time.
* **Localized Tips Module:** Users can submit and upvote tips tied to a specific geographic area (e.g., "Best roofer in [zip code]," "Watch for basement flooding on Silhavy Road after heavy spring downpours").
* **Material and Vendor Log:** A simple database, with a digital interface to introduce CRUD functionality, to log key home information (paint colors, flooring types, appliance model numbers), contact information for trusted service providers or links to relevant articles/videos, if available.

#### Out-of-scope (for the minimal viable artifact)

* Automated parts ordering or e-commerce integration.
* Recommendations for replacement appliances or service providers based on environmental factors/user input.
* Professional contractor bidding or scheduling services.
* Integration with smart home devices (IoT sensors for leaks, thermostat, etc.).
* AI-driven diagnostics for maintenance issues.

---

### Success Metrics

* **Task Completion Rate:** A high percentage of users mark scheduled maintenance tasks as "complete" within a defined time frame.
* **Knowledge Acquisition:** Users spend a measurable amount of time viewing and interacting with the task profiles, localized tips and, over time, become more competent with different homeowner skillsets.
* **Community Engagement:** A consistent flow of new, unique tips and questions submitted to the localized tips module.
* **User Retention:** A high rate of users returning to the app or website after the initial setup; especially when it’s a “seasonal” home maintenance task (such as cleaning gutters before the first frost).

---

### Minimal Viable Artifact (MVA)

The MVA possesses three deliverables:

1.  A basic **Personalized Maintenance (PM) Schedule** that generates a simple checklist based on user inputs.
2.  A **Task Profiles** feature with basic, pre-written guides for 10-15 common maintenance items.
3.  A **Localized Tips Module** with a simple submission and upvoting system.

This design is simple, but also provides homeowners with a powerful, proactive tool to combat maintenance neglect, which will make for a better homeownership experience.

---

### Iterative Design Approach

Development will progress via the repeatable steps below:

**Conduct User Research → Establish requirements → Feature Prototyping → Community Feedback/UX testing → Refinement → REPEAT cycle.**

The first few cycles will focus on creating an intuitive setup process and populating the core maintenance task database with information provided by users. Subsequent cycles will introduce the localized tips, with feedback from early adopters guiding the expansion of features. This approach ensures that the tool grows alongside its users' needs, starting with the essentials and building a collaborative knowledge base over time.

### System Sketch


---

### Evidence Base

* Harvard Joint Center for Housing Studies. (2025). *Improving America's Housing.* Harvard University. https://www.jchs.harvard.edu/improving-americas-housing-2025
* Adekunle, A. A., & Agboola, M. F. (2023). Factors Affecting Building Maintenance Practices: Review. *ResearchGate.* https://www.researchgate.net/publication/376182890_Factors_Affecting_Building_Maintenance_Practices_Review
* NC State Extension Publications. (2023, October 31). *Preventative Home Maintenance.* https://content.ces.ncsu.edu/preventative-home-maintenance.
* GA College of Family and Consumer Sciences. (2021, June). *Home Maintenance Checklist.* https://www.fcs.uga.edu/docs/HomeMaintChecklist_update_6.21.pdf.
* University of Minnesota Extension. (n.d.). *Home maintenance and safety.* https://extension.umn.edu/caring-your-home/home-maintenance-and-safety.
* CSU Global. (2022, July 8). *Your Simple Home Maintenance Checklist for Summer.* https://csuglobal.edu/blog/life-prerequisites-your-simple-home-maintenance-checklist-summer.

---

### Risk Register

| Risk Description | Impact | Likelihood | Mitigation |
| :--- | :--- | :--- | :--- |
| The combination of multiple inputs for the personalized Preventative Maintenance Schedule is too complex and leads to inaccurate schedules. | High | Medium | Focus on the most common inputs (home age, climate zone) for the MVA. Use a dynamic design to add complexity in future iterations, if necessary. Thoroughly test the algorithm for the initial 10-15 maintenance items. |
| Lackluster community participation causes low quality localized tips and users searching for answers elsewhere. | Medium | Medium | Incentivize early adopters to contribute tips, possibly with "trusted contributor" badges and emphasize the potential increased customer outreach they could achieve. Seed the database with high-quality, pre-researched tips for a variety of regions/situations to demonstrate value and set a standard. |
| Legal liability issues arise if a user attempts a DIY task based on a tip and causes damage or injury. | High | Low | Implement a strong, easy-to-understand disclaimer stating that tips are user-generated and should be used with caution. Include a "consult a professional" advisory on all DIY tips. |
| The price of developing and maintaining the MVA exceeds the budget due to technical debt and unforeseen issues. | Medium | Medium | Do not exceed the defined MVA scope to avoid feature creep. Conduct thorough testing to prevent costly bugs and rework. |
| The user interface (UI) for the MVA is of low quality, leading to low user retention. | Medium | Medium | Prioritize a crisp, intuitive design during the prototyping and UX testing phases. Focus on core user flows (onboarding, schedule, tasks, tips) and validate with user feedback. Take user feedback and make changes, redo UX testing and repeat until satisfied. |
