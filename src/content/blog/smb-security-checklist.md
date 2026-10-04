---
title: "SMB Security Checklist: 10 Steps to Protect Your Business Today"
description: "A practical, prioritized security checklist for small and mid-size businesses. No jargon, no enterprise-only tools — just actionable steps you can start on Monday."
date: 2025-09-05
author: "Orion's Guard"
tags: ["SMB Security", "Checklist", "Getting Started"]
draft: false
---

Most small businesses don't have a dedicated security team. What they do have is a real attack surface, real threat actors targeting them, and the same regulatory obligations as much larger organizations. The good news: a focused effort on the fundamentals closes the majority of your risk.

This checklist is ordered by impact. Start at the top and work down.

---

## ☑ 1. Enable Multi-Factor Authentication (MFA) Everywhere

**Impact: Very High. Effort: Low.**

The single most impactful security control available to any organization is multi-factor authentication. MFA prevents the majority of account takeover attacks — including those using stolen or phished passwords.

**Priority order for MFA rollout:**
1. Email accounts (especially if on Microsoft 365 or Google Workspace)
2. Financial accounts (banking, payroll, accounting software)
3. Administrative accounts (domain registrar, DNS, cloud hosting)
4. SaaS tools (CRM, HR software, project management)
5. Everything else

Use an authenticator app (Google Authenticator, Microsoft Authenticator, or Authy) rather than SMS-based MFA whenever possible. SMS MFA is better than nothing but is vulnerable to SIM-swapping attacks.

---

## ☑ 2. Deploy a Password Manager

**Impact: High. Effort: Low-Medium.**

Password reuse is one of the most common attack vectors for small business breaches. When one service gets breached, attackers try those credentials everywhere. A password manager solves this by making it practical to use unique, strong passwords for every account.

**Recommended options for SMBs:**
- **1Password Business** — excellent team sharing and admin controls
- **Bitwarden** (open source, self-hostable, very affordable)
- **Keeper** — strong compliance reporting features

Require all employees to use the company password manager for any business account.

---

## ☑ 3. Keep Software and Systems Patched

**Impact: Very High. Effort: Medium.**

The majority of successful attacks exploit known vulnerabilities for which patches already exist. Patch management is not glamorous, but it's essential.

**Minimum requirements:**
- Enable automatic updates for operating systems on all devices
- Enable automatic updates for web browsers
- Set a monthly cadence for reviewing and applying patches to business applications
- Don't forget network devices — router and switch firmware needs patching too

---

## ☑ 4. Back Up Your Data — and Test Those Backups

**Impact: Very High (especially for ransomware defense). Effort: Medium.**

Ransomware works by encrypting your data and demanding payment for the decryption key. Organizations with clean, tested backups can recover without paying the ransom. Organizations without them often can't.

**Backup requirements:**
- **3-2-1 rule**: 3 copies, 2 different media types, 1 offsite/offline
- Backups must be isolated from your network — a backup drive that's always connected will be encrypted by ransomware along with everything else
- **Test restoration quarterly** — a backup you've never tested is a backup you can't trust
- For critical data: consider immutable backup solutions (backups that can't be modified or deleted even by an admin)

---

## ☑ 5. Train Employees to Recognize Phishing

**Impact: High. Effort: Medium.**

Phishing is the most common initial access vector for small business breaches. Your employees need to know what modern phishing looks like — which is increasingly sophisticated and no longer limited to obvious Nigerian prince emails.

**Minimum training requirements:**
- Annual security awareness training for all employees
- Phishing simulation exercises (send simulated phishing emails to test and train)
- Clear reporting procedure: "If I think this is phishing, I do X"
- Special focus: business email compromise (BEC), invoice fraud, and executive impersonation

---

## ☑ 6. Control Who Has Access to What

**Impact: High. Effort: Medium.**

Least-privilege access means every user has exactly the access they need for their job — and nothing more. This limits the blast radius of a compromised account or a malicious insider.

**Actions:**
- Audit all user accounts quarterly — remove accounts for departed employees immediately
- Separate administrative accounts from daily-use accounts
- No shared accounts — every user gets their own login
- Document who has admin access to critical systems
- Use role-based access control in your key applications

---

## ☑ 7. Secure Your Wi-Fi and Network

**Impact: Medium-High. Effort: Low-Medium.**

Your network is the connective tissue of your business. Weak network security gives attackers a foothold into everything connected to it.

**Requirements:**
- Use WPA3 (or at minimum WPA2) on all Wi-Fi networks
- Separate guest Wi-Fi from your business network
- Separate IoT devices (smart TVs, cameras, printers) onto their own network segment
- Change default admin passwords on all network devices
- Disable remote management on your router unless specifically needed

---

## ☑ 8. Deploy Endpoint Detection and Response (EDR)

**Impact: High. Effort: Medium.**

Legacy antivirus is no longer sufficient. Modern endpoint protection (EDR) products detect behavior-based threats that signature-based tools miss — including ransomware, fileless malware, and supply chain attacks.

**Options at SMB scale:**
- **Microsoft Defender for Business** — included with Microsoft 365 Business Premium; solid protection at low marginal cost
- **SentinelOne Singularity** — industry-leading detection, SMB-friendly pricing available
- **CrowdStrike Falcon Go** — strong option for growing businesses

Centralized management visibility is important — you need to be able to see what's happening across all endpoints, not just on individual machines.

---

## ☑ 9. Create and Test an Incident Response Plan

**Impact: High when you need it. Effort: Medium.**

When something goes wrong — and eventually something will — having a documented response plan is the difference between a contained incident and a catastrophic one.

**Your incident response plan must answer:**
- Who is the incident response coordinator?
- Who do we call first? (IT contact, legal counsel, cyber insurance provider)
- What systems do we isolate immediately?
- How do we communicate internally during an incident?
- What are our regulatory notification obligations?
- Where do we go if our email system is compromised?

Review and tabletop-test this plan annually.

---

## ☑ 10. Review Your Cyber Insurance Coverage

**Impact: Financial protection. Effort: Low.**

Cyber insurance doesn't prevent breaches, but it significantly limits their financial impact. Most cyber policies cover incident response costs, legal fees, regulatory fines, customer notification, and business interruption.

**When reviewing your policy, ask:**
- Does the policy require specific security controls to be in place? (Many do — and if you don't have them, you may not be covered)
- What's the ransomware sublimit?
- Does the policy cover business email compromise and wire fraud?
- What's the incident response process?

A cyber insurance broker who specializes in cyber (not a generalist) is worth using for this.

---

## Where to Start

If this list feels overwhelming, here's the prioritized first week:

**Day 1:** Enable MFA on email and financial accounts  
**Day 2-3:** Deploy a password manager, require it for all employees  
**Day 4:** Verify backups are running and test one restore  
**Day 5:** Review admin account access and remove any departed employees  

These five actions, completed in a week, eliminate a significant percentage of your risk. Everything else can be layered in from there.

---

*Orion's Guard can help you build a security program that covers all ten steps — designed for your team size, budget, and industry. [Book a free discovery call →](/contact/)*

