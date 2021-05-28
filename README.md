![krsh](assets/logo.svg)

<p align="center"> A declarative Kubeflow Management Tool inspired by <a href="https://github.com/hashicorp/terraform">Terraform</a></p>

---

**KRSH** (pronounce, krush) is a tool that allows you to declaratively manage Kubeflow's pipelines. By managing Kubeflow Pipeline through KRSH, developers can reduce the cost of managing Pipeline Versions and deploy pipelines much faster than ever before. KRSH is very much inspired by [Hashicorp's](https://www.hashicorp.com/) Terraform, which allows you to manage your Kubeflow Pipeline in a way similar to how Terraform manages Cloud declaratively. Similar to Terraform, KRSH can deploy pipelines through **Write, Plan, and Apply Cycle**. Also, since KRSH provides the KRSH Project Boilerplate through the `krsh create` command, the developer who develops the pipeline no longer needs to worry about which project structure to choose to manage the Kubeflow Pipeline.

## Usage

The image below shows a very simple example of using KRSH. Actually, that's all. Click [GETTING_STARTED.md](./GETTING_STARTED.md) for more information.

![commands](assets/commands.gif)



## Install

**Easy way**
```bash
pip install krsh
```

**Manually way**
```bash
git clone https://github.com/riiid/krsh
cd ./krsh
pip install -e .
```

## Contribution

We welcome any form of contribution. If you're new to KRSH, read [CONTRIBUTING.md](CONTRIBUTING.md). You can submit any PR that can improve project, report bugs in project, or submit an Issue to request that you add new features.

## License

[Apache License, Version 2.0](LICENSE)