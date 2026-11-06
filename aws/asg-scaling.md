AWS Auto Scaling Groups (ASGs) support four distinct types of dynamic scaling policies. Each type handles the evaluation period and execution logic differently based on how aggressively or automatically you want your infrastructure to respond. [1, 2]

---

## 1. Target Tracking Scaling (The "Thermostat" Approach)

This is the default and easiest policy type. You select a metric (like average CPU utilization) and set a target value (like 60%). AWS automatically creates the underlying CloudWatch alarms and manages the evaluation periods for you. [3, 4, 5, 6, 7]

- How it works: If CPU utilization is at 40%, it terminates instances. If it hits 80%, it adds instances to bring the average back to 60%. [8, 9]
- Best for: Standard web applications with predictable or gradual traffic changes. [10, 11, 12]
- Evaluation control: AWS locks the evaluation periods behind the scenes (usually a tight window for scaling out, and a longer window for scaling in) so you do not have to configure them manually.

## 2. Step Scaling (The "Graduated Response" Approach)

Step scaling increases or decreases capacity based on the size of the metric breach. You manually attach a CloudWatch alarm and define "steps" or tiers for scaling. [13, 14, 15, 16, 17]

- How it works: You configure a CloudWatch alarm to fire if CPU stays above 70% for 3 out of 5 evaluation periods. You then define steps:
    
    - If CPU is between 70% and 80% → add 1 instance.
    - If CPU is between 80% and 90% → add 2 instances.
    - If CPU is above 90% → add 4 instances. [18, 19, 20, 21]
    
- Best for: Systems that experience massive, unpredictable spikes where a massive load requires a massive, immediate infrastructure response. [22, 23]
- Evaluation control: Fully customizable. You own the CloudWatch alarm configuration, period, evaluation periods, and datapoints to alarm. [24]

## 3. Simple Scaling (The "Legacy" Approach)

Simple scaling is an older version of Step scaling. It triggers a single fixed change based on a single metric threshold. [25, 26, 27]

- How it works: If CPU breaches 70% for 3 out of 5 evaluation periods, add exactly 1 instance.
- The drawback: Once triggered, the policy locks the ASG and enters a cooldown period (e.g., 5 minutes). While in cooldown, the ASG ignores all further alarm breaches. If your traffic tripled during that time, Simple scaling cannot respond until the cooldown expires, whereas Step scaling can continually evaluate and scale up further.
- Best for: Legacy architectures. In almost all modern use cases, Step scaling should be preferred over Simple scaling. [28, 29, 30, 31, 32]

## 4. Predictive Scaling (The "Machine Learning" Approach)

Predictive scaling uses machine learning to analyze your historical traffic patterns (up to 14 days of data) and forecasts future demand, scheduling capacity changes _before_ the traffic actually arrives. [33, 34, 35, 36, 37]

- How it works: If AWS detects that your traffic spikes every day at 9:00 AM, it will proactively launch EC2 instances at 8:30 AM so they are fully booted and warm by the time the rush hits.
- Best for: Applications with strong cyclical patterns (e.g., business tools busy Monday–Friday, or food delivery apps busy at lunchtime). [38]
- Evaluation control: It does not use real-time CloudWatch evaluation windows for its proactive scaling. Instead, it re-evaluates its forecast model daily. It is highly recommended to pair Predictive scaling with Target Tracking to catch unexpected, non-cyclical spikes. [39]

---

## 🔄 Summary Comparison

|Policy Type|Configuration Effort|Setup Control over Evaluation Periods?|Handles Massive Spikes Quickly?|
|---|---|---|---|
|Target Tracking|Minimal (Set & Forget)|No (Managed by AWS)|Good|
|Step Scaling|Medium|Yes (Full manual control)|Excellent (Scale by tier)|
|Simple Scaling|Medium|Yes (Full manual control)|Poor (Blocked by cooldown)|
|Predictive Scaling|Minimal|No (Algorithmic forecasting)|Poor for sudden anomalies|

Which of these policies aligns best with your application's workload? I can help write the Terraform block or CLI command to implement it.