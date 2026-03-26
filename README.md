# Project Beyla-I
### Year 2025/2026, Group 4
### Authors
- Piotr Andres
- Antoni Dulewicz 
- Wojciech Fortuna 
- Paweł Podedworny

---
## 1. Introduction
The primary objective of this project is to develop a comprehensive case study focused on modern application observability using Grafana Beyla within an AI-driven management framework. Traditionally, instrumenting an application for deep visibility requires significant manual effort, such as modifying source code or deploying language-specific agents, which often necessitates service redeployments.

This project explores a more efficient alternative: eBPF-based auto-instrumentation. By leveraging Grafana Beyla, we demonstrate how to capture essential RED metrics (Rate, Error, and Duration) and distributed traces without modifying a single line of the application’s code or configuration. In this architecture, Grafana Beyla serves as the core observability engine, processing telemetry from the Linux kernel to provide insights into HTTP/S and gRPC services.

Furthermore, the project implements an advanced control loop where a Large Language Model (LLM) interacts with the application through a Model Context Protocol (MCP) Server. This setup allows for intelligent application management and automated configuration guided by AI. The resulting telemetry, captured non-intrusively by Beyla, is then streamed to Grafana for visualization and performance analysis. The final outcome is a live demonstration of a resilient system where autonomous AI control, kernel-level observability, and high-fidelity visualization converge.

---
## 2. Theoretical background/technology stack
### 2.1. Extended Berkeley Packet Filter (eBPF)
Extended Berkeley Packet Filter (eBPF) is a powerful technology built into the Linux kernel that allows sandboxed programs to run inside the operating system kernel without requiring changes to the kernel source code or loading kernel modules.

eBPF programs are safe, as they are compiled for their own Virtual Machine instruction set and then can run in sandbox environment that pre-verifies each loaded program for safe memory access and finite execution time.

The eBPF code is loaded from ordinary programs running in user space. Both kernel and user space programs can share information through set of communication machanisms that are provided by the eBPF specification, such as ring buffers, arrays, hash maps, etc.

![alt text](image.png)

### 2.2. Grafana Beyla and Auto-instrumentation
Grafana Beyla represents a modern approach to application telemetry by utilizing eBPF to provide zero-code auto-instrumentation capabilities. Unlike traditional APM tools that require developers to manually embed language-specific SDKs, Beyla attaches directly to tracepoints at the kernel level.

This tool natively inspects application behavior across a wide spectrum of runtime environments, including Go, C/C++, Rust, Python, and Java. By intercepting network traffic and system calls right at the operating system layer, Beyla automatically calculates and exports essential RED metrics (Rate, Error, Duration).

Furthermore, it efficiently maps these network requests to generate OpenTelemetry-compatible distributed trace spans for both HTTP/S and gRPC communications. The fundamental architectural advantage is the complete elimination of manual code modifications, which significantly reduces operational overhead.

### 2.3. Model Context Protocol (MCP) and Large Language Models (LLM)
The management and operational interaction layer of this project is driven by advanced language models, creating an automated workflow. Advanced foundational models, such as Claude, Cursor, or Chat GPT, function as the primary engine for analyzing environment parameters and managing the application.

To facilitate this autonomous operational strategy, the LangChain framework serves as the core orchestration middleware. It effectively maintains context, manages prompts, and seamlessly executes the required external tools without the need for manual intervention.

The Model Context Protocol (MCP) Server acts as the critical bridge in this architecture, translating the intents of the LLM into highly specific API interactions. This standardized protocol ensures that the language model can reliably communicate with the target application and modify its state.

<img src="image2.png" width="300" alt="llm-mcp diagram">

### 2.4. Telemetry and Visualization Stack
To make the high-resolution data captured by Beyla actionable, the architecture employs a robust telemetry pipeline built around the OpenTelemetry specification. This standardization ensures maximum interoperability and seamless telemetry data collection across all monitored services.

Within this pipeline, Prometheus functions as the highly efficient time-series database. It is responsible for aggregating and storing the exposed application metrics and network trace data.

Grafana provides a comprehensive visualization layer, rendering the collected data into highly intuitive dashboards in real-time. Additionally, Grafana Assistance makes it easier for operators to manage the system and interpret the gathered data.

---
## 3. Case study concept description

### Application
The core concept of this case study revolves around deploying a baseline target application that will serve as the subject of an integrated experiment with the LLM. Once the target environment is provisioned, the selected large language model autonomously takes over the management role. Utilizing the LangChain framework and the MCP Server, the artificial intelligence generates commands to the application, simulates workloads, and executes predefined operational scenarios based on customized prompts.

### Observability
Simultaneously, the observability layer relies on Grafana Beyla, which operates entirely in the background at the Linux kernel level. This eBPF-based tool passively monitors all network interactions and system responses without requiring any modifications to the application code. As the LLM interacts with the application, Beyla captures deep RED metrics, and Prometheus continuously aggregates this massive telemetry stream, maintaining a historical record of the operational state in an OpenTelemetry-compatible format.

### Visualization
In the final stage of the pipeline, the data is forwarded to the visualization layer. Grafana (either OSS or Cloud version) seamlessly synthesizes these raw metrics retrieved from Prometheus, presenting them on comprehensive dashboards. These visualizations, further supported by Grafana Assistance, actively correlate the actions performed by the LLM with the resulting performance metrics, demonstrating the effectiveness of eBPF-based observability.

---
## 4. Case study high level architecture

The proposed system architecture is organized into three distinct layers: the application layer, the observability layer, and the visualization layer. This layered structure ensures a clear separation of responsibilities between system control, monitoring, and data presentation. The architecture combines AI-driven application management with non-intrusive observability and real-time visualization, forming a cohesive and modern approach to system analysis.

Unlike the conceptual description presented in the previous section, this section focuses on the structural organization of the system and the relationships between its components, emphasizing its layered architecture and data flows.

To better illustrate the relationships between the components and the overall system structure, the high-level architecture is shown in the diagram below.

![High-level architecture](image3.png)

### Application Layer

The application layer represents the core operational part of the system and is responsible for executing application logic under the control of an AI agent. This layer consists of a Large Language Model (LLM), the LangChain orchestration framework, the Model Context Protocol (MCP) Server, and the target application.

These components form a control pipeline in which the LLM generates high-level instructions based on predefined prompts or scenarios. The LangChain framework manages the execution flow and context of these instructions, while the MCP Server translates them into specific API calls or executable actions. The target application then performs these actions, such as handling requests, simulating workloads, or triggering predefined behaviors.

As a result, the application layer establishes an automated control loop in which the AI agent dynamically influences the behavior of the system without requiring manual intervention.

### Observability Layer

The observability layer is responsible for collecting telemetry data from the running application in a fully passive and non-intrusive manner. This layer is built around Grafana Beyla, which leverages eBPF technology to monitor application behavior at the Linux kernel level.

Beyla operates independently of the application code and does not require any instrumentation or configuration changes. It captures essential RED metrics (Rate, Error, Duration) as well as basic trace information by observing network interactions and system calls.

Importantly, this layer does not interfere with the execution of the application. Instead, it continuously collects high-fidelity telemetry data reflecting the real-time impact of the actions performed by the AI agent in the application layer.

### Visualization Layer

The visualization layer provides a user-facing interface for analyzing and interpreting the collected telemetry data. This layer is implemented using Grafana, which presents the monitored metrics through interactive dashboards.

Grafana enables real-time visualization of application performance, including request rates, error occurrences, and response times. By correlating these metrics with the actions initiated by the AI agent, users can evaluate the effectiveness of automated management and observe system behavior under different scenarios.

### System Flow Overview

The architecture defines two primary flows: the control flow and the monitoring flow.

The control flow originates from the LLM and propagates through the LangChain framework and the MCP Server before reaching the target application. This flow represents the active influence of the AI agent on the system, enabling automated execution of operational scenarios.

In parallel, the monitoring flow captures the effects of these actions. The behavior of the application is passively observed by Grafana Beyla, and the collected data is forwarded to the visualization layer, where it is presented in Grafana dashboards.

This dual-flow design creates a feedback loop in which AI-driven actions can be directly correlated with system performance metrics, enabling comprehensive analysis and evaluation.

## 5. Case study detailed architecture

## 6. Environment configuration description

## 7. Installation method

## 8. Demo deployment steps

### 8a. Configuration set-up

### 8b. Data preparation

## 9. Demo description

### 9a. Execution procedure

### 9b. Results presentation

### 10. Summary – conclusions

### 11. References
