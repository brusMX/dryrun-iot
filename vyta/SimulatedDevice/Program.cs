namespace SimulatedDevice
{
    using System;
    using System.Text;
    using System.Threading.Tasks;
    using Microsoft.Azure.Devices.Client;
    using Newtonsoft.Json;
    using System.IO;

    public class Program
    {
        private const string IotHubUri = "BrakeLabRuleHub.azure-devices.net";
        private const string DeviceKey = "DEVICE_KEY";
        private const string DeviceId = "vysFirstDevice";
        private const string DataFileName = "PATH_TO_DATA";
        private static DeviceClient _deviceClient;

        private static async void SendDeviceToCloudMessagesAsync(int runs)
        {
            try
            {
                var data = System.IO.File.ReadAllLines(DataFileName);
                foreach(var d in data)
                { 
                    var line = d.Split(',');
                    var currentTime = DateTime.Now.ToString("yyyy/MM/dd HH:mm:ss");
                    var eventData = new
                    {
                        liftOperation = Guid.NewGuid(),
                        eventTime = currentTime,
                        speed = line[1],
                        torque = line[2],
                        volts = line[3]
                    };

                    var messageString = JsonConvert.SerializeObject(eventData);
                    var message = new Message(Encoding.ASCII.GetBytes(messageString));

                    await _deviceClient.SendEventAsync(message);
                    Console.WriteLine("{0} > Sending message: {1}", currentTime, messageString);

                    await Task.Delay(1000);
                }
                await Task.Delay(30000);
                int num = runs++;
                Console.WriteLine($"\nStarting simulation #{num}");
                SendDeviceToCloudMessagesAsync(num);
            }
            catch (FileNotFoundException ex)
            {
                Console.WriteLine($"Cannot find {DataFileName}");
            }
        }

        private static void Main(string[] args)
        {
            Console.WriteLine("Simulated device\n");
            _deviceClient = DeviceClient.Create(IotHubUri, new DeviceAuthenticationWithRegistrySymmetricKey(DeviceId, DeviceKey), TransportType.Mqtt);
            _deviceClient.ProductInfo = "HappyPath_Simulated-CSharp";
            
            SendDeviceToCloudMessagesAsync(0);
            Console.ReadLine();
        }
    }
}
