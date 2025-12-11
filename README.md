# Distributed Computing with Ray on Azure VMs

This repository contains the code and documentation for a small distributed computing project built for a Computer Networks course. The project uses:

- Two **Azure Virtual Machines** in the same Virtual Network (VNet)
- The **Ray** distributed execution framework
- **Python 3**
- **Pillow** (for image processing)

There are two main demonstrations:

1. A **CPU-heavy parallel task** that shows load balancing across the cluster.
2. A **distributed image-processing workload** that applies a Gaussian blur to real images across both VMs.

---

## Architecture Overview

### Nodes

- **headVM**
  - Role: Ray **head node** (cluster manager)
  - Example private IP: `10.1.1.5`
- **workerVM**
  - Role: Ray **worker node**
  - Example private IP: `10.1.1.6`

Both VMs are in the same Azure Virtual Network and communicate using private IPs. The Ray cluster uses the head node’s private IP and a default Ray port (e.g. `10.1.1.5:6379`).

### High-Level Diagram

```text
                   (Your Laptop)
                  SSH / VS Code
                        |
                        v
                +------------------+
                |      headVM      |
                |  Ray Head Node   |
                | 10.1.1.5 (priv)  |
                +---------+--------+
                          |
                   Azure Virtual Network
                    (Private IP traffic)
                          |
                +---------v--------+
                |    workerVM      |
                | Ray Worker Node  |
                | 10.1.1.6 (priv)  |
                +------------------+
