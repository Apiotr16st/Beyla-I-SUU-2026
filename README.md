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

eBPF programs are safe, as they are complied for their own Virtual Machine instruction set and then can run in sandbox environment that pre-verifies each loaded program for safe memory access and finite execution time.

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

## 3. Case study concept description

### Application
The core concept of this case study revolves around deploying a baseline target application that will serve as the subject of an integrated experiment with the LLM. Once the target environment is provisioned, the selected large language model autonomously takes over the management role. Utilizing the LangChain framework and the MCP Server, the artificial intelligence generates commands to the application, simulates workloads, and executes predefined operational scenarios based on customized prompts.

### Observability
Simultaneously, the observability layer relies on Grafana Beyla, which operates entirely in the background at the Linux kernel level. This eBPF-based tool passively monitors all network interactions and system responses without requiring any modifications to the application code. As the LLM interacts with the application, Beyla captures deep RED metrics, and Prometheus continuously aggregates this massive telemetry stream, maintaining a historical record of the operational state in an OpenTelemetry-compatible format.

### Visualization
In the final stage of the pipeline, the data is forwarded to the visualization layer. Grafana (either OSS or Cloud version) seamlessly synthesizes these raw metrics retrieved from Prometheus, presenting them on comprehensive dashboards. These visualizations, further supported by Grafana Assistance, actively correlate the actions performed by the LLM with the resulting performance metrics, demonstrating the effectiveness of eBPF-based observability.

## 4. Case study high level architecture

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
