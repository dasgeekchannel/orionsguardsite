---
title: "HIPAA Basics: What Every Small Business Needs to Know"
description: "HIPAA isn't just for hospitals. If your business handles health information in any context, here's what the law requires and how to get compliant."
date: 2025-09-10
author: "Orion's Guard"
tags: ["HIPAA", "Compliance", "Healthcare"]
draft: false
---

The Health Insurance Portability and Accountability Act (HIPAA) is frequently misunderstood as a regulation that applies only to hospitals and large healthcare systems. In practice, it applies to a much broader universe of organizations — including many small businesses that may not realize they're covered.

## Who Does HIPAA Actually Cover?

HIPAA applies to two categories of organizations:

**Covered Entities:**
- Healthcare providers (doctors, dentists, therapists, pharmacies, hospitals)
- Health plans (insurance companies, HMOs, employer-sponsored health plans)
- Healthcare clearinghouses (organizations that process health information between providers and payers)

**Business Associates:**
This is where many small businesses get caught. A Business Associate is any organization that creates, receives, maintains, or transmits Protected Health Information (PHI) on behalf of a Covered Entity. This includes:
- Medical billing companies
- IT service providers and MSPs that handle healthcare client data
- Cloud storage providers used by healthcare organizations
- Legal and accounting firms serving healthcare clients
- Marketing and PR firms working with healthcare organizations
- Transcription services, answering services, and call centers
- Software vendors whose products process PHI

If you provide services to a healthcare organization and your work involves access to patient health information — even incidentally — you are likely a Business Associate and HIPAA applies to you.

## What Is Protected Health Information (PHI)?

PHI is any individually identifiable health information that is:
1. Created or received by a Covered Entity or Business Associate
2. Related to an individual's past, present, or future health condition, treatment, or payment

PHI includes a long list of identifiers — not just the health condition itself, but name, address, date of birth, Social Security number, phone number, email address, and even IP addresses when linked to health information.

**Electronic PHI (ePHI)** is PHI stored, transmitted, or processed electronically — which means most PHI in modern healthcare environments.

## The Three HIPAA Rules

### Privacy Rule
Governs the use and disclosure of PHI. Key requirements:
- Use only the minimum necessary PHI for any given purpose
- Provide patients with a Notice of Privacy Practices
- Give patients the right to access and amend their records
- Obtain patient authorization for non-routine disclosures

### Security Rule
Governs the protection of ePHI. Requires:
- Administrative safeguards (policies, procedures, training, access management)
- Physical safeguards (facility controls, workstation security, device controls)
- Technical safeguards (access controls, audit controls, encryption, transmission security)

The Security Rule is risk-based — it doesn't prescribe specific technologies but requires you to implement "reasonable and appropriate" safeguards based on a risk assessment.

### Breach Notification Rule
Requires notification when ePHI is breached:
- Affected individuals: within 60 days of discovery
- HHS (Department of Health and Human Services): same 60-day window; breaches affecting 500+ individuals must be reported immediately
- Media: for breaches affecting 500+ individuals in a state or jurisdiction

## The HIPAA Security Rule Checklist for Small Businesses

**Administrative Safeguards:**
- [ ] Complete a formal risk analysis
- [ ] Implement a risk management plan based on the analysis
- [ ] Designate a Privacy Officer and Security Officer (can be the same person)
- [ ] Conduct HIPAA training for all workforce members
- [ ] Implement access management procedures (who gets access to what PHI, how it's granted/revoked)
- [ ] Execute Business Associate Agreements (BAAs) with all vendors who handle PHI

**Physical Safeguards:**
- [ ] Control physical access to facilities where ePHI is processed
- [ ] Implement workstation security policies
- [ ] Establish procedures for mobile device and media management (including disposal)

**Technical Safeguards:**
- [ ] Implement unique user IDs for all system access
- [ ] Implement automatic logoff for systems handling ePHI
- [ ] Enable encryption for ePHI at rest and in transit
- [ ] Maintain audit logs of all access to ePHI
- [ ] Implement integrity controls to detect unauthorized modification

## Business Associate Agreements (BAAs)

If you're a Business Associate, you must have a signed BAA with each Covered Entity client before you can handle their PHI. If you're a Covered Entity, you must have BAAs with all your Business Associates.

A BAA must include:
- Permitted uses and disclosures of PHI
- Requirements to use appropriate safeguards
- Obligation to report breaches
- Requirements to flow down obligations to subcontractors
- Procedures for PHI return or destruction upon contract termination

Most major cloud services that can be configured for HIPAA compliance (Microsoft 365, Google Workspace, AWS, Azure) will provide BAAs on request. Make sure you have them before using these services with PHI.

## Penalties

HIPAA penalties are tiered based on the level of culpability:

| Tier | Violation | Minimum | Maximum |
|------|-----------|---------|---------|
| 1 | Unknowing | $100/violation | $50,000/violation |
| 2 | Reasonable cause | $1,000/violation | $50,000/violation |
| 3 | Willful neglect, corrected | $10,000/violation | $50,000/violation |
| 4 | Willful neglect, not corrected | $50,000/violation | $1.9M/year |

Penalties are assessed per violation category per year. Organizations that have suffered a breach due to inadequate security controls face significant financial exposure.

---

*Orion's Guard provides HIPAA compliance consulting for small businesses, MSPs, and healthcare adjacent organizations. We make compliance achievable without breaking your budget. [Book a free discovery call →](/contact/)*

