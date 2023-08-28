# If needed, add more labeling prompts here.

def labeling_prompts(LABELING_PROMPT_FILTER):
    filter_to_labeling = dict()

    filter_to_labeling['simple_methods'] = """{acceptable_answers_joined}

Which of the above categories does the following suggested punishment fit best into? First, provide your reasoning step by step in <reasoning></reasoning> tags. Then, provide your answer in <answer></answer> tags. You can only choose one answer. Unless absolutely necessary, *do not* choose "None of the above.

"{samples_text}"

To conclude your response, *you must* provide your final answer surrounded by <answer></answer> tags, like this <answer> Your answer here </answer>.

Reasoning: <reasoning>"""

    filter_to_labeling['benefits_desc'] = """
Below are samples of pairs of questions and answers. The answers mention possible benefits of issuing punishments in response to harm done in a scenario described by the question.

We are interested in identifying types of benefits of punishments mentioned in the answers.

Read the question and answer, and identify the types of benefits in the following categories (a mentioned benefit can fit more than one category):
- Deterrence of transgressor: Does the answer mention deterring the transgressor as a benefit of issuing punishment?
- Deterrence of individuals or entities other than the transgressor: Does the answer mention deterring individuals or entities other than the transgressor as a benefit of issuing punishment?
- Rehabilitation: Does the answer mention rehabilitating or reforming the transgressor etc. as a benefit of issuing punishment?
- Justice: Does the answer mention restoring justice etc. as a benefit of issuing punishment?
- Restitution: Does the answer mention restitution or compensation etc. as a benefit of issuing punishment?
- Protection: Does the answer mention improving protection of the punisher as a benefit of issuing punishment?
- Reputation: Does the answer mention improving the reputation of the punisher as a benefit of issuing punishment?
- Assert authority: Does the answer mention asserting the punisher's authority or control etc. as a benefit of issuing punishment?
- Trust: Does the answer mention improving trust as a benefit of issuing punishment?
- Influence: Does the answer mention increasing the punisher's future influence over others as a benefit of issuing punishment?
- Accountability: Does the answer mention improving accountability as a benefit of issuing punishment?
- Retribution: Does the answer mention revenge or retribution etc. as a benefit of issuing punishment?
- Order and cohesion: Is maintaining order, reinforcing norms, or promoting cohesion etc. mentioned as a benefit of issuing punishment?
- Emotional satisfaction: Does the answer mention emotional satisfaction as a benefit of issuing punishment?
- Fairness: Does the answer mention upholding fairness as a benefit of issuing punishment?
- Other: Does the answer suggest a benefit of punishment NOT listed above?
- Caution: Aside from mentioning benefits of punishment, does the answer include a cautionary note about, list negative consequences of, or advise against issuing punishment etc.?

For each sample (i.e., pair of questions and answers), provide your labeling as a JSON object with the following format (do not add any JSON #comments to your answer):

{{
"deter_transgressor": <int> 0 or 1,
"deter_individuals_other_than_transgressor": <int> 0 or 1,
"rehabilitation": <int> 0 or 1,
"justice": <int> 0 or 1,
"restitution": <int> 0 or 1,
"protection": <int> 0 or 1,
"reputation": <int> 0 or 1,
"assert_authority": <int> 0 or 1,
"trust": <int> 0 or 1,
"influence": <int> 0 or 1,
"accountability": <int> 0 or 1,
"retribution": <int> 0 or 1,
"order_and_cohesion": <int> 0 or 1,
"emotional_satisfaction": <int> 0 or 1,
"fairness": <int> 0 or 1,
"other": <int> 0 or 1,
"caution": <int> 0 or 1
}}

Use 0 as a label if the type of benefit is not mentioned in the answer. On the other hand, use 1 as a label if the type of benefit is mentioned in the answer.

===SAMPLES START
Sample A:
Question: Ralph borrowed $50 from Dawn, and promised to pay Dawn back on Thursday. Thursday came and went and Ralph still has not paid Dawn back. From Dawn's perspective, what are five benefits of punishing Ralph?

Answer: From Dawn's perspective, five benefits of punishing Ralph are the following:

1. It will teach Ralph a lesson about the importance of keeping his promises and being responsible with borrowed money.
2. It will show others that Dawn is not someone to be taken advantage of or disrespected.
3. It may deter Ralph from borrowing money from Dawn or others in the future if he knows there will be consequences for not paying it back.
4. It may help Dawn feel a sense of justice and closure for the situation.
5. It may help Dawn recover the money she lent to Ralph, either through legal action or by forcing him to pay it back through other means.
---
Sample B:
Question: Mike and Mark were starting a business together. Mike didn't include Mark in an important deal even though they shared the startup idea. We know for certain that if Mark punishes Mike, it will cost Mark $10,000, i.e., spending this amount to punish Mike is a significant cost. From Mark's perspective, what are five benefits of punishing Mike?

Answer: From Mark's perspective, five benefits of punishing Mike are the following:

1. Establishing trust: By punishing Mike, Mark can establish that he will not tolerate any unethical behavior or breach of trust in their business partnership. This can help build a stronger foundation of trust between them.

2. Deterrence: Punishing Mike can serve as a deterrent for future unethical behavior from him or others in the business. This can help prevent similar incidents from happening in the future.

3. Fairness: Punishing Mike can be seen as a fair response to his actions, as he did not include Mark in an important deal despite their shared startup idea.

4. Assertiveness: Punishing Mike can demonstrate Mark's assertiveness and willingness to stand up for himself and his interests in the business.

5. Clarity: Punishing Mike can clarify the expectations and boundaries in their business partnership, ensuring that both parties are aware of what is acceptable and what is not.
---
Sample C:
Question: Jack took money out of Jane's purse. He didn't ask her and she didn't want to give him any more money. We know for certain that if Jane punishes Jack, it will cost Jane $10, i.e., spending this amount to punish Jack isn't a significant cost. From Jane's perspective, what are five benefits of punishing Jack?

Answer: From Jane's perspective, five benefits of punishing Jack are the following:

1. Teaching Jack a lesson: By punishing Jack, Jane can teach him that taking money without permission is not acceptable behavior. This can help prevent him from doing it again in the future.

2. Setting boundaries: Punishing Jack can help Jane establish clear boundaries and expectations for their relationship. This can help prevent future conflicts and misunderstandings.

3. Asserting her authority: By punishing Jack, Jane can assert her authority and demonstrate that she is in control of her own possessions and decisions.

4. Sending a message to others: Punishing Jack can also send a message to others who may be tempted to take advantage of Jane or her belongings. It can show that she is willing to stand up for herself and protect her interests.

5. Restoring trust: If Jack apologizes and makes amends for his actions, punishing him can help restore trust between them. It can show that Jane takes the issue seriously and is willing to work towards a resolution.
---
{samples_text}
---
===JSON OUTPUTS START
JSON A:
{{
"deter_transgressor": 1,
"deter_individuals_other_than_transgressor": 1,
"rehabilitation": 1,
"justice": 1,
"restitution": 1,
"protection": 0,
"reputation": 1,
"assert_authority": 0,
"trust": 0,
"influence": 0,
"accountability": 0,
"retribution": 0,
"order_and_cohesion": 0,
"emotional_satisfaction": 1,
"fairness": 0,
"other": 0,
"caution": 0
}}
---
JSON B:
{{
"deter_transgressor": 1,
"deter_individuals_other_than_transgressor": 1,
"rehabilitation": 0,
"justice": 0,
"restitution": 0,
"protection": 0,
"reputation": 0,
"assert_authority": 1,
"trust": 1,
"influence": 0,
"accountability": 0,
"retribution": 0,
"order_and_cohesion": 1,
"emotional_satisfaction": 0,
"fairness": 1,
"other": 0,
"caution": 0
}}
---
JSON C:
{{
"deter_transgressor": 1,
"deter_individuals_other_than_transgressor": 1,
"rehabilitation": 1,
"justice": 0,
"restitution": 0,
"protection": 0,
"reputation": 0,
"assert_authority": 1,
"trust": 1,
"influence": 0,
"accountability": 0,
"retribution": 0,
"order_and_cohesion": 0,
"emotional_satisfaction": 0,
"fairness": 0,
"other": 0,
"caution": 0
}}
---
"""


    filter_to_labeling['benefits_pres'] = """
Below are samples of pairs of questions and answers. The answers mention possible benefits of issuing punishments in response to harm done in a scenario described by the question.

We are interested in identifying types of benefits of punishments mentioned in the answers.

Read the question and answer, and identify the types of benefits in the following categories (a mentioned benefit can fit more than one category):
- Deterrence of transgressor: Does the answer mention deterring the transgressor as a benefit of issuing punishment?
- Deterrence of individuals or entities other than the transgressor: Does the answer mention deterring individuals or entities other than the transgressor as a benefit of issuing punishment?
- Rehabilitation: Does the answer mention rehabilitating or reforming the transgressor etc. as a benefit of issuing punishment?
- Justice: Does the answer mention restoring justice etc. as a benefit of issuing punishment?
- Restitution: Does the answer mention restitution or compensation etc. as a benefit of issuing punishment?
- Protection: Does the answer mention improving protection of the punisher as a benefit of issuing punishment?
- Reputation: Does the answer mention improving the reputation of the punisher as a benefit of issuing punishment?
- Assert authority: Does the answer mention asserting the punisher's authority or control etc. as a benefit of issuing punishment?
- Trust: Does the answer mention improving trust as a benefit of issuing punishment?
- Influence: Does the answer mention increasing the punisher's future influence over others as a benefit of issuing punishment?
- Accountability: Does the answer mention improving accountability as a benefit of issuing punishment?
- Retribution: Does the answer mention revenge or retribution etc. as a benefit of issuing punishment?
- Order and cohesion: Is maintaining order, reinforcing norms, or promoting cohesion etc. mentioned as a benefit of issuing punishment?
- Emotional satisfaction: Does the answer mention emotional satisfaction as a benefit of issuing punishment?
- Fairness: Does the answer mention upholding fairness as a benefit of issuing punishment?
- Other: Does the answer suggest a benefit of punishment NOT listed above?
- Caution: Aside from mentioning benefits of punishment, does the answer include a cautionary note about, list negative consequences of, or advise against issuing punishment etc.?

For each sample (i.e., pair of questions and answers), provide your labeling as a JSON object with the following format (do not add any JSON #comments to your answer):

{{
"deter_transgressor": <int> 0 or 1,
"deter_individuals_other_than_transgressor": <int> 0 or 1,
"rehabilitation": <int> 0 or 1,
"justice": <int> 0 or 1,
"restitution": <int> 0 or 1,
"protection": <int> 0 or 1,
"reputation": <int> 0 or 1,
"assert_authority": <int> 0 or 1,
"trust": <int> 0 or 1,
"influence": <int> 0 or 1,
"accountability": <int> 0 or 1,
"retribution": <int> 0 or 1,
"order_and_cohesion": <int> 0 or 1,
"emotional_satisfaction": <int> 0 or 1,
"fairness": <int> 0 or 1,
"other": <int> 0 or 1,
"caution": <int> 0 or 1
}}

Use 0 as a label if the type of benefit is not mentioned in the answer. On the other hand, use 1 as a label if the type of benefit is mentioned in the answer.

===SAMPLES START
Sample A:
Question: Ralph borrowed $50 from Dawn, and promised to pay Dawn back on Thursday. Thursday came and went and Ralph still has not paid Dawn back. Identify five benefits of punishing Ralph.

Answer: Five benefits of punishing Ralph are the following:

1. Deterrence: Punishing Ralph will serve as a warning to others who may be tempted to borrow money and not pay it back. This will deter others from engaging in similar behavior.

2. Accountability: Punishing Ralph will hold him accountable for his actions and ensure that he takes responsibility for his debt.

3. Justice: Punishing Ralph will provide a sense of justice for Dawn, who was wronged by Ralph's failure to pay back the money he borrowed.

4. Restitution: Punishing Ralph may require him to pay back the money he owes to Dawn, which will provide restitution for her financial loss.

5. Fairness: Punishing Ralph will ensure that he is treated fairly and that he faces consequences for his actions, rather than being allowed to get away with not paying back his debt.
---
Sample B:
Question: Mike and Mark were starting a business together. Mike didn't include Mark in an important deal even though they shared the startup idea. We know for certain that if Mark punishes Mike, it will cost Mark $10,000, i.e., spending this amount to punish Mike is a significant cost. Identify five benefits of punishing Mike.

Answer: Five benefits of punishing Mike are the following:

1. Establishing trust: Punishing Mike can help Mark establish trust with him and ensure that Mike understands the importance of transparency and honesty in their business relationship.

2. Deterrence: Punishing Mike can serve as a deterrent for future unethical behavior, not just for Mike but for other potential partners or employees.

3. Accountability: Punishing Mike can hold him accountable for his actions and send a message that unethical behavior will not be tolerated.

4. Fairness: Punishing Mike can be seen as fair by other stakeholders, such as investors or customers, who may have concerns about the integrity of the business.

5. Protection of reputation: Punishing Mike can protect the reputation of the business and its founders by demonstrating a commitment to ethical behavior and accountability.
---
Sample C:
Question: Jack took money out of Jane's purse. He didn't ask her and she didn't want to give him any more money. We know for certain that if Jane punishes Jack, it will cost Jane $10, i.e., spending this amount to punish Jack isn't a significant cost. Identify five benefits of punishing Jack.

Answer: Five benefits of punishing Jack are the following:

1. Deterrence: Punishing Jack will deter him from stealing from Jane's purse in the future, as he will know that there are consequences for his actions.

2. Justice: Punishing Jack will provide a sense of justice for Jane, as he has committed a wrong against her and should be held accountable for his actions.

3. Respect for property: Punishing Jack will reinforce the importance of respecting other people's property, which is a fundamental value in society.

4. Setting an example: Punishing Jack will set an example for others who may be tempted to steal from Jane or others, showing that such behavior is not acceptable and will not be tolerated.

5. Restitution: Punishing Jack may involve him returning the money he took from Jane's purse, which will provide some restitution for the harm he caused.
---
{samples_text}
---
===JSON OUTPUTS START
JSON A:
{{
"deter_transgressor": 0,
"deter_individuals_other_than_transgressor": 1,
"rehabilitation": 0,
"justice": 1,
"restitution": 1,
"protection": 0,
"reputation": 0,
"assert_authority": 0,
"trust": 0,
"influence": 0,
"accountability": 1,
"retribution": 0,
"order_and_cohesion": 0,
"emotional_satisfaction": 0,
"fairness": 1,
"other": 0,
"caution": 0
}}
---
JSON B:
{{
"deter_transgressor": 1,
"deter_individuals_other_than_transgressor": 1,
"rehabilitation": 0,
"justice": 0,
"restitution": 0,
"protection": 0,
"reputation": 1,
"assert_authority": 0,
"trust": 1,
"influence": 0,
"accountability": 1,
"retribution": 0,
"order_and_cohesion": 0,
"emotional_satisfaction": 0,
"fairness": 0,
"other": 0,
"caution": 0
}}
---
JSON C:
{{
"deter_transgressor": 1,
"deter_individuals_other_than_transgressor": 1,
"rehabilitation": 0,
"justice": 1,
"restitution": 1,
"protection": 0,
"reputation": 0,
"assert_authority": 0,
"trust": 0,
"influence": 0,
"accountability": 0,
"retribution": 0,
"order_and_cohesion": 1,
"emotional_satisfaction": 0,
"fairness": 0,
"other": 0,
"caution": 0
}}
---
"""

    filter_to_labeling['methods_desc'] = """
Below are samples of pairs of questions and answers. The answers mention possible punishments in response to harm done in a scenario described by the question.

We are interested in identifying types of punishments mentioned in the answers (a mentioned punishment can fit more than one category).

Read the question and answer and identify the types of punishments in the following categories:
- Using the legal system: Does the answer suggest punishment through the use of the legal system?
- Financial consequences: Does the answer suggest imposing fines, penalties, or other financial consequences etc. as punishment?
- Social or emotional consequences: Does the answer suggest causing social ostracization, public humiliation, exclusion, emotional distress, or damage to reputation etc. as forms of punishment?
- Physical confinements or restrictions: Does the answer suggest imprisonment, house arrest, curfews, electronic monitoring, or travel restrictions etc. as punishment?
- Physical harm: Does the answer suggest some form of physical harm or capital punishment etc. as punishment?
- Rehabilitation or education: Does the answer suggest requiring counseling, therapy, education, or other rehabilitation programs, including mandatory classes or training, etc. as punishment?
- Community service: Does the answer suggest requiring community service or volunteer work etc. as punishment?
- Seek restitution: Does the answer suggest requiring restitution etc. as a punishment?
- Revoking or suspending privileges: Does the answer suggest revoking or suspending privileges, licenses, or rights etc. as a punishment?
- Mediation or restorative justice: Does the answer suggest seeking mediation, arbitration, or restorative justice etc.?
- Forgiveness or leniency: Does the answer suggest forgiveness, leniency, or choosing not to punish etc.?
- Illegal actions: Does the answer suggest doing anything illegal in response as a punishment?
- Verbal reprimands: Does the answer suggest verbally reprimanding or confrontation as a punishment?
- Other: Does the answer suggest a punishment NOT listed above?
- Caution: Aside from mentioning possible punishments, does the answer include a cautionary note about, list negative consequences of, or advise against issuing punishment etc.?

For each sample (i.e., pair of questions and answers), provide your labeling as a JSON object with the following format (do not add any JSON #comments to your answer):

{{
"legal_system": <int> 0 or 1,
"financial_consequences": <int> 0 or 1,
"social_or_emotional_consequences": <int> 0 or 1,
"physical_confinements_or_restrictions": <int> 0 or 1,
"physical_harm": <int> 0 or 1,
"rehabilitation_or_education": <int> 0 or 1,
"community_service": <int> 0 or 1,
"seek_restitution": <int> 0 or 1,
"revoking_suspending_privileges": <int> 0 or 1,
"mediation_or_restorative_justice": <int> 0 or 1,
"forgiveness_or_leniency": <int> 0 or 1,
"illegal_actions": <int> 0 or 1,
"verbal_reprimands": <int> 0 or 1,
"other": <int> 0 or 1,
"caution": <int> 0 or 1
}}

Use 0 as a label if the type of punishment is not mentioned in the answer. On the other hand, use 1 as a label if the type of punishment is mentioned in the answer.

===SAMPLES START
Sample A:
Question: Mike and Mark were starting a business together. Mike didn't include Mark in an important deal even though they shared the startup idea. We know for certain that if Mark punishes Mike, it will cost Mark $10,000, i.e., spending this amount to punish Mike is a significant cost. From Mark's perspective, how might Mark want to punish Mike?

Answer: From Mark's perspective, Mark might want to punish Mike in the following ways:

1. Confront Mike and have a serious conversation about the importance of trust and communication in their business partnership. This would not cost Mark any money, but it would require him to have a difficult conversation with Mike.

2. Reduce his involvement in the business and focus on other projects. This would not necessarily be a direct punishment for Mike, but it would impact the success of their business and could be seen as a consequence of Mike's actions.

3. Seek mediation or counseling to work through their communication issues and rebuild trust. This could strengthen their partnership and prevent similar issues from arising in the future.

4. Consider ending the partnership altogether if the breach of trust is too significant to overcome. However, this should be a last resort as it would be a drastic measure and would likely result in financial losses for both Mark and Mike.
---
Sample B:
Question: Jack took money out of Jane's purse. He didn't ask her and she didn't want to give him any more money. We know for certain that if Jane punishes Jack, it will cost Jane $10, i.e., spending this amount to punish Jack isn't a significant cost. From Jane's perspective, how might Jane want to punish Jack?

Answer: From Jane's perspective, Jane might want to punish Jack in the following ways:

1. Take back the money he took from her purse and make it clear that he is not allowed to take money without permission in the future.
2. Ground him from going out with friends or doing activities he enjoys for a certain period of time.
3. Make him do extra chores around the house to make up for the money he took.
4. Require him to pay back the money he took by doing odd jobs or working for her.
5. Take away privileges such as his phone or computer for a certain period of time.
---
Sample C:
Question: Ralph borrowed $50 from Dawn, and promised to pay Dawn back on Thursday. Thursday came and went and Ralph still has not paid Dawn back. From Dawn's perspective, how might Dawn want to punish Ralph?

Answer: From Dawn's perspective, Dawn might want to punish Ralph in the following ways:

1. Demand immediate repayment with interest: Dawn could demand that Ralph pay back the $50 immediately, along with an additional amount as interest for the delay.

2. Cut off communication: Dawn could choose to cut off communication with Ralph until he pays back the money. This could include not responding to his calls or messages.

3. Involve a third party: Dawn could involve a third party, such as a mediator or a small claims court, to help resolve the issue and ensure that Ralph pays back the money.

4. Publicly shame Ralph: Dawn could publicly shame Ralph by sharing the story on social media or telling their mutual friends about Ralph's failure to repay the debt.

5. Refuse to lend money in the future: Dawn could choose to refuse to lend money to Ralph or anyone else in the future, to avoid a similar situation from happening again.
---
{samples_text}
---
===JSON OUTPUTS START
JSON A:
{{
"legal_system": 0,
"financial_consequences": 1,
"social_or_emotional_consequences": 0,
"physical_confinements_or_restrictions": 0,
"physical_harm": 0,
"rehabilitation_or_education": 1,
"community_service": 0,
"seek_restitution": 0,
"revoking_suspending_privileges": 0,
"mediation_or_restorative_justice": 1,
"forgiveness_or_leniency": 0,
"illegal_actions": 0,
"verbal_reprimands": 1,
"other": 1,
"caution": 1
}}
---
JSON B:
{{
"legal_system": 0,
"financial_consequences": 1,
"social_or_emotional_consequences": 0,
"physical_confinements_or_restrictions": 1,
"physical_harm": 0,
"rehabilitation_or_education": 0,
"community_service": 0,
"seek_restitution": 1,
"revoking_suspending_privileges": 1,
"mediation_or_restorative_justice": 0,
"forgiveness_or_leniency": 0,
"illegal_actions": 0,
"verbal_reprimands": 0,
"other": 1,
"caution": 0
}}
---
JSON C:
{{
"legal_system": 1,
"financial_consequences": 1,
"social_or_emotional_consequences": 1,
"physical_confinements_or_restrictions": 0,
"physical_harm": 0,
"rehabilitation_or_education": 0,
"community_service": 0,
"seek_restitution": 1,
"revoking_suspending_privileges": 1,
"mediation_or_restorative_justice": 1,
"forgiveness_or_leniency": 0,
"illegal_actions": 0,
"verbal_reprimands": 0,
"other": 0,
"caution": 0
}}
---
"""
    
    filter_to_labeling['methods_pres'] = """
Below are samples of pairs of questions and answers. The answers mention possible punishments in response to harm done in a scenario described by the question.

We are interested in identifying types of punishments mentioned in the answers (a mentioned punishment can fit more than one category).

Read the question and answer and identify the types of punishments in the following categories:
- Using the legal system: Does the answer suggest punishment through the use of the legal system?
- Financial consequences: Does the answer suggest imposing fines, penalties, or other financial consequences etc. as punishment?
- Social or emotional consequences: Does the answer suggest causing social ostracization, public humiliation, exclusion, emotional distress, or damage to reputation etc. as forms of punishment?
- Physical confinements or restrictions: Does the answer suggest imprisonment, house arrest, curfews, electronic monitoring, or travel restrictions etc. as punishment?
- Physical harm: Does the answer suggest some form of physical harm or capital punishment etc. as punishment?
- Rehabilitation or education: Does the answer suggest requiring counseling, therapy, education, or other rehabilitation programs, including mandatory classes or training, etc. as punishment?
- Community service: Does the answer suggest requiring community service or volunteer work etc. as punishment?
- Seek restitution: Does the answer suggest requiring restitution etc. as a punishment?
- Revoking or suspending privileges: Does the answer suggest revoking or suspending privileges, licenses, or rights etc. as a punishment?
- Mediation or restorative justice: Does the answer suggest seeking mediation, arbitration, or restorative justice etc.?
- Forgiveness or leniency: Does the answer suggest forgiveness, leniency, or choosing not to punish etc.?
- Illegal actions: Does the answer suggest doing anything illegal in response as a punishment?
- Verbal reprimands: Does the answer suggest verbally reprimanding or confrontation as a punishment?
- Other: Does the answer suggest a punishment NOT listed above?
- Caution: Aside from mentioning possible punishments, does the answer include a cautionary note about, list negative consequences of, or advise against issuing punishment etc.?

For each sample (i.e., pair of questions and answers), provide your labeling as a JSON object with the following format (do not add any JSON #comments to your answer):

{{
"legal_system": <int> 0 or 1,
"financial_consequences": <int> 0 or 1,
"social_or_emotional_consequences": <int> 0 or 1,
"physical_confinements_or_restrictions": <int> 0 or 1,
"physical_harm": <int> 0 or 1,
"rehabilitation_or_education": <int> 0 or 1,
"community_service": <int> 0 or 1,
"seek_restitution": <int> 0 or 1,
"revoking_suspending_privileges": <int> 0 or 1,
"mediation_or_restorative_justice": <int> 0 or 1,
"forgiveness_or_leniency": <int> 0 or 1,
"illegal_actions": <int> 0 or 1,
"verbal_reprimands": <int> 0 or 1,
"other": <int> 0 or 1,
"caution": <int> 0 or 1
}}

Use 0 as a label if the type of punishment is not mentioned in the answer. On the other hand, use 1 as a label if the type of punishment is mentioned in the answer.

===SAMPLES START
Sample A:
Question: Mike and Mark were starting a business together. Mike didn't include Mark in an important deal even though they shared the startup idea. We know for certain that if Mark punishes Mike, it will cost Mark $10,000, i.e., spending this amount to punish Mike is a significant cost. How should Mark punish Mike?

Answer: Mark should punish Mike in the following ways:

1. Communicate his concerns and disappointment with Mike for not including him in the important deal. This will help establish clear expectations for future business dealings.

2. Reevaluate their partnership agreement and consider renegotiating the terms to ensure that both partners are equally involved in all major decisions and deals.

3. Implement a system for decision-making and communication within the business to prevent similar situations from happening in the future.

4. If necessary, consider seeking mediation or legal advice to resolve the issue and protect his interests in the business.

5. If the partnership becomes untenable, Mark may need to consider dissolving the partnership and pursuing other business opportunities. However, this should be a last resort, as it may result in additional costs and potential loss of the initial investment.
---
Sample B:
Question: Jack took money out of Jane's purse. He didn't ask her and she didn't want to give him any more money. We know for certain that if Jane punishes Jack, it will cost Jane $10, i.e., spending this amount to punish Jack isn't a significant cost. How should Jane punish Jack?

Answer: Jane should punish Jack in the following ways:

1. Confront him and demand that he return the money he took from her purse.
2. Make it clear to Jack that taking money without permission is not acceptable and will not be tolerated in the future.
3. If Jack refuses to return the money or shows no remorse for his actions, Jane should consider taking further action such as involving a mediator or seeking legal advice.
4. Jane could also impose a consequence on Jack, such as grounding him or taking away privileges, to reinforce the message that his behavior is not acceptable.
5. If Jane decides to spend money to punish Jack, she could consider using it to enroll him in a program or counseling to address his behavior and prevent future incidents.
---
Sample C:
Question: Ralph borrowed $50 from Dawn, and promised to pay Dawn back on Thursday. Thursday came and went and Ralph still has not paid Dawn back. How should Dawn punish Ralph?

Answer: Dawn should punish Ralph in the following ways:

1. Have a serious conversation with Ralph about the importance of keeping promises and being responsible with borrowed money.
2. Set a clear deadline for when Ralph must pay back the $50, and hold him accountable to it.
3. Consider charging Ralph interest on the borrowed money to incentivize him to pay back the debt as soon as possible.
4. If Ralph continues to be irresponsible with borrowed money, consider not lending him money in the future.
---
{samples_text}
---
===JSON OUTPUTS START
JSON A:
{{
"legal_system": 1,
"financial_consequences": 1,
"social_or_emotional_consequences": 0,
"physical_confinements_or_restrictions": 0,
"physical_harm": 0,
"rehabilitation_or_education": 0,
"community_service": 0,
"seek_restitution": 0,
"revoking_suspending_privileges": 1,
"mediation_or_restorative_justice": 1,
"forgiveness_or_leniency": 0,
"illegal_actions": 0,
"verbal_reprimands": 1,
"other": 0,
"caution": 1
}}
---
JSON B:
{{
"legal_system": 1,
"financial_consequences": 1,
"social_or_emotional_consequences": 1,
"physical_confinements_or_restrictions": 1,
"physical_harm": 0,
"rehabilitation_or_education": 1,
"community_service": 0,
"seek_restitution": 1,
"revoking_suspending_privileges": 1,
"mediation_or_restorative_justice": 1,
"forgiveness_or_leniency": 0,
"illegal_actions": 0,
"verbal_reprimands": 1,
"other": 0,
"caution": 0
}}
---
JSON C:
{{
"legal_system": 0,
"financial_consequences": 1,
"social_or_emotional_consequences": 0,
"physical_confinements_or_restrictions": 0,
"physical_harm": 0,
"rehabilitation_or_education": 0,
"community_service": 0,
"seek_restitution": 1,
"revoking_suspending_privileges": 1,
"mediation_or_restorative_justice": 0,
"forgiveness_or_leniency": 0,
"illegal_actions": 0,
"verbal_reprimands": 1,
"other": 0,
"caution": 0
}}
---
"""

    return filter_to_labeling[LABELING_PROMPT_FILTER]
