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

## 3. Case study concept description, Application/Observability/Vizualization

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
