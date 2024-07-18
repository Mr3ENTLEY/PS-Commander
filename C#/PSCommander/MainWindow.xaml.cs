using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using System.Windows;

namespace PSCommander
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private async void ExecuteCommand_Click(object sender, RoutedEventArgs e)
        {
            string command = CommandTextBox.Text;
            if (!string.IsNullOrEmpty(command))
            {
                if (HelpToggle.IsChecked == true)
                {
                    command = $"help {command}";
                }
                await ExecutePowerShellCommand(command);
            }
            else
            {
                MessageBox.Show("Please enter a command.", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        private async Task ExecutePowerShellCommand(string command)
        {
            try
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

                using (Process process = new Process())
                {
                    process.StartInfo = startInfo;
                    process.OutputDataReceived += (sender, args) =>
                    {
                        Dispatcher.Invoke(() =>
                        {
                            if (args.Data != null)
                            {
                                OutputTextBox.AppendText(args.Data + Environment.NewLine);
                            }
                        });
                    };
                    process.ErrorDataReceived += (sender, args) =>
                    {
                        Dispatcher.Invoke(() =>
                        {
                            if (args.Data != null)
                            {
                                OutputTextBox.AppendText("ERROR: " + args.Data + Environment.NewLine);
                            }
                        });
                    };

                    process.Start();
                    process.BeginOutputReadLine();
                    process.BeginErrorReadLine();
                    await process.WaitForExitAsync();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
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

    public static class ProcessExtensions
    {
        public static Task WaitForExitAsync(this Process process)
        {
            var tcs = new TaskCompletionSource<bool>();
            process.EnableRaisingEvents = true;
            process.Exited += (sender, args) => tcs.TrySetResult(true);
            if (process.HasExited) tcs.TrySetResult(true);
            return tcs.Task;
        }
    }
}
