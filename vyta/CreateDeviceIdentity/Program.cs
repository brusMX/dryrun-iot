namespace CreateDeviceIdentity
{
    using System;
    using System.Configuration;
    using System.Threading.Tasks;
    using Microsoft.Azure.Devices;
    using Microsoft.Azure.Devices.Common.Exceptions;

    public class Program
    {
        private static RegistryManager _registryManager;
        private const string ConnectionString = "CONNECTION_STRING";
        private const string DeviceId = "vysFirstDevice";

        private static void Main(string[] args)
        {
            _registryManager = RegistryManager.CreateFromConnectionString(ConnectionString);
            AddDeviceAsync().Wait();
            Console.ReadLine();
        }

        private static async Task AddDeviceAsync()
        {
            Device device;
            try
            {
                device = await _registryManager.AddDeviceAsync(new Device(DeviceId));
                Console.WriteLine($"Success! New device {DeviceId} registered");
            }
            catch (DeviceAlreadyExistsException)
            {
                device = await _registryManager.GetDeviceAsync(DeviceId);
                Console.WriteLine($"Success! Existing device {DeviceId} already registered");
            }
            catch (Exception e)
            {
                Console.WriteLine($"register device failed: {e.Message}");
                throw;
            }

            Console.WriteLine($"device key : {device.Authentication.SymmetricKey.PrimaryKey}");
        }
        
    }
}
