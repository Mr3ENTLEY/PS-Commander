using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Collections.Generic;

namespace PSCommander
{
    public partial class MainWindow : Window
    {
        private Dictionary<string, string> predefinedCommands;
        private Process currentProcess;

        public MainWindow()
        {
            InitializeComponent();
            InitializePredefinedCommands();
        }

        private void InitializePredefinedCommands()
        {
            predefinedCommands = new Dictionary<string, string>
            {
                { "Get-Process", "Get-Process" },
                { "Get-Service", "Get-Service" },
                { "Get-Network", "IPCONFIG /all" },
                { "Get-Command", "Get-Command" },
                { "Get-User", "Get-LocalUser" }
            };
        }

        private async void ExecuteCommand_Click(object sender, RoutedEventArgs e)
        {
            string command = CommandTextBox.Text.Trim();
            if (!string.IsNullOrEmpty(command))
            {
                if (HelpToggle.IsChecked == true)
                {
                    command = $"Get-Help {command}";
                }
                ExecuteButton.IsEnabled = false;
                ProgressIndicator.Visibility = Visibility.Visible;
                await ExecutePowerShellCommand(command);
                ExecuteButton.IsEnabled = true;
                ProgressIndicator.Visibility = Visibility.Hidden;
            }
            else
            {
                MessageBox.Show("Please enter a command.", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        private void PredefinedCommand_Click(object sender, RoutedEventArgs e)
        {
            if (sender is Button button && predefinedCommands.ContainsKey(button.Content.ToString()))
            {
                CommandTextBox.Text = predefinedCommands[button.Content.ToString()];
            }
        }

        private async Task ExecutePowerShellCommand(string command)
        {
            try
            {
                OutputTextBox.Clear();

                await Task.Run(() =>
                {
                    ProcessStartInfo startInfo = new ProcessStartInfo
                    {
                        FileName = "powershell.exe",
                        Arguments = $"-Command \"{command}\"",
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false,
                        CreateNoWindow = true
                    };

                    using (currentProcess = new Process())
                    {
                        currentProcess.StartInfo = startInfo;
                        currentProcess.OutputDataReceived += (sender, args) =>
                        {
                            Dispatcher.Invoke(() =>
                            {
                                if (args.Data != null)
                                {
                                    OutputTextBox.AppendText(args.Data + Environment.NewLine);
                                }
                            });
                        };
                        currentProcess.ErrorDataReceived += (sender, args) =>
                        {
                            Dispatcher.Invoke(() =>
                            {
                                if (args.Data != null)
                                {
                                    OutputTextBox.AppendText("ERROR: " + args.Data + Environment.NewLine);
                                }
                            });
                        };

                        currentProcess.Start();
                        currentProcess.BeginOutputReadLine();
                        currentProcess.BeginErrorReadLine();
                        currentProcess.WaitForExit();
                    }
                });
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                currentProcess = null;
            }
        }

        private void StopCommand_Click(object sender, RoutedEventArgs e)
        {
            if (currentProcess != null && !currentProcess.HasExited)
            {
                currentProcess.Kill();
                OutputTextBox.AppendText("Command execution stopped." + Environment.NewLine);
            }
        }

        private void ClearOutput_Click(object sender, RoutedEventArgs e)
        {
            OutputTextBox.Clear();
        }

        private void ExportToCsv_Click(object sender, RoutedEventArgs e)
        {
            string outputPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "CommandOutput.csv");
            File.WriteAllText(outputPath, OutputTextBox.Text);
            MessageBox.Show($"Output exported to {outputPath}", "Export Successful", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }
}
