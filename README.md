# MSIFanControl

**MSIFanControl** offers a user-friendly interface and automated scripts to control MSI laptop fans on Linux systems.

## 🚀 Features

- Simple UI for fan control
- Automated scripts for convenience
- Tested on select MSI laptops and Linux distros

## 📋 Prerequisites

- [Task](https://taskfile.dev/) — Please install Task before proceeding.

## 🛠️ Installation & Update

1. **Clone or download** this repository.
2. **Ensure Task is installed** on your system.

## ▶️ Running MSIFanControl

Run the following command in your terminal:

```sh
task run
```

This will start MSIFanControl.

## 🐞 Troubleshooting

- **Error:**

  ```
  FileNotFoundError: [Errno 2] No such file or directory: '/sys/kernel/debug/ec/ec0/io'
  ```

  **Solution:**  
  Run:

  ```sh
  sudo modprobe ec_sys write_support=1
  ```

- **Note:**  
  A reboot may be required after the first installation.

## 💻 Supported Laptop Models

- MSI GF65 Thin 9SD

## 🐧 Supported Linux Distros

- Zorin OS

## 🙏 Acknowledgements

- [YoyPa/isw](https://github.com/YoyPa/isw)
- [YoCodingMonster/OpenFreezeCenter](https://github.com/YoCodingMonster/OpenFreezeCenter)
