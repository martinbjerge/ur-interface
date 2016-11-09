using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UniversalRobotsConnect
{
    public class StructConverter
    {
        // We use this function to provide an easier way to type-agnostically call the GetBytes method of the BitConverter class.
        // This means we can have much cleaner code below.
        private static byte[] TypeAgnosticGetBytes(object o)
        {
            if (o is int)
                return BitConverter.GetBytes((int)o);
            if (o is uint)
                return BitConverter.GetBytes((uint)o);
            if (o is long)
                return BitConverter.GetBytes((long)o);
            if (o is ulong)
                return BitConverter.GetBytes((ulong)o);
            if (o is short)
                return BitConverter.GetBytes((short)o);
            if (o is ushort)
                return BitConverter.GetBytes((ushort)o);
            if (o is byte || o is sbyte)
                return new byte[] { (byte)o };
            throw new ArgumentException("Unsupported object type found");
        }

        private static string GetFormatSpecifierFor(object o)
        {
            if (o is int) return "l";
            if (o is uint) return "L";
            if (o is long) return "q";
            if (o is ulong) return "Q";
            if (o is short) return "h";
            if (o is ushort) return "H";
            if (o is byte) return "B";
            if (o is sbyte) return "b";
            throw new ArgumentException("Unsupported object type found");
        }

        /// <summary>
        /// Convert a byte array into an array of objects based on Python's "struct.unpack" protocol.
        /// </summary>
        /// <param name="fmt">A "struct.pack"-compatible format string</param>
        /// <param name="bytes">An array of bytes to convert to objects</param>
        /// <returns>Array of objects.</returns>
        /// <remarks>You are responsible for casting the objects in the array back to their proper types.</remarks>
        public static object[] Unpack(string fmt, byte[] bytes)
        {
            Debug.WriteLine("Format string is length {0}, {1} bytes provided.", fmt.Length, bytes.Length);

            // First we parse the format string to make sure it's proper.
            if (fmt.Length < 1) throw new ArgumentException("Format string cannot be empty.");

            bool endianFlip = false;
            if (fmt.Substring(0, 1) == "<")
            {
                Debug.WriteLine("  Endian marker found: little endian");
                // Little endian.
                // Do we need to flip endianness?
                if (BitConverter.IsLittleEndian == false) endianFlip = true;
                fmt = fmt.Substring(1);
            }
            else if (fmt.Substring(0, 1) == ">")
            {
                Debug.WriteLine("  Endian marker found: big endian");
                // Big endian.
                // Do we need to flip endianness?
                if (BitConverter.IsLittleEndian == true) endianFlip = true;
                fmt = fmt.Substring(1);
            }

            // Now, we find out how long the byte array needs to be
            int totalByteLength = 0;
            foreach (char c in fmt.ToCharArray())
            {
                Debug.WriteLine("  Format character found: {0}", c);
                switch (c)
                {
                    case 'q':
                    case 'Q':
                        totalByteLength += 8;
                        break;
                    case 'l':
                    case 'L':
                        totalByteLength += 4;
                        break;
                    case 'h':
                    case 'H':
                        totalByteLength += 2;
                        break;
                    case 'b':
                    case 'B':
                    case 'x':
                        totalByteLength += 1;
                        break;
                    default:
                        throw new ArgumentException("Invalid character found in format string.");
                }
            }

            Debug.WriteLine("Endianness will {0}be flipped.", (object)(endianFlip == true ? "" : "NOT "));
            Debug.WriteLine("The byte array is expected to be {0} bytes long.", totalByteLength);

            // Test the byte array length to see if it contains as many bytes as is needed for the string.
            if (bytes.Length != totalByteLength) throw new ArgumentException("The number of bytes provided does not match the total length of the format string.");

            // Ok, we can go ahead and start parsing bytes!
            int byteArrayPosition = 0;
            List<object> outputList = new List<object>();
            byte[] buf;

            Debug.WriteLine("Processing byte array...");
            foreach (char c in fmt.ToCharArray())
            {
                switch (c)
                {
                    case 'q':
                        outputList.Add((object)(long)BitConverter.ToInt64(bytes, byteArrayPosition));
                        byteArrayPosition += 8;
                        Debug.WriteLine("  Added signed 64-bit integer.");
                        break;
                    case 'Q':
                        outputList.Add((object)(ulong)BitConverter.ToUInt64(bytes, byteArrayPosition));
                        byteArrayPosition += 8;
                        Debug.WriteLine("  Added unsigned 64-bit integer.");
                        break;
                    case 'l':
                        outputList.Add((object)(int)BitConverter.ToInt32(bytes, byteArrayPosition));
                        byteArrayPosition += 4;
                        Debug.WriteLine("  Added signed 32-bit integer.");
                        break;
                    case 'L':
                        outputList.Add((object)(uint)BitConverter.ToUInt32(bytes, byteArrayPosition));
                        byteArrayPosition += 4;
                        Debug.WriteLine("  Added unsignedsigned 32-bit integer.");
                        break;
                    case 'h':
                        outputList.Add((object)(short)BitConverter.ToInt16(bytes, byteArrayPosition));
                        byteArrayPosition += 2;
                        Debug.WriteLine("  Added signed 16-bit integer.");
                        break;
                    case 'H':
                        outputList.Add((object)(ushort)BitConverter.ToUInt16(bytes, byteArrayPosition));
                        byteArrayPosition += 2;
                        Debug.WriteLine("  Added unsigned 16-bit integer.");
                        break;
                    case 'b':
                        buf = new byte[1];
                        Array.Copy(bytes, byteArrayPosition, buf, 0, 1);
                        outputList.Add((object)(sbyte)buf[0]);
                        byteArrayPosition++;
                        Debug.WriteLine("  Added signed byte");
                        break;
                    case 'B':
                        buf = new byte[1];
                        Array.Copy(bytes, byteArrayPosition, buf, 0, 1);
                        outputList.Add((object)(byte)buf[0]);
                        byteArrayPosition++;
                        Debug.WriteLine("  Added unsigned byte");
                        break;
                    case 'x':
                        byteArrayPosition++;
                        Debug.WriteLine("  Ignoring a byte");
                        break;
                    default:
                        throw new ArgumentException("You should not be here.");
                }
            }
            return outputList.ToArray();
        }

        /// <summary>
        /// Convert an array of objects to a byte array, along with a string that can be used with Unpack.
        /// </summary>
        /// <param name="items">An object array of items to convert</param>
        /// <param name="LittleEndian">Set to False if you want to use big endian output.</param>
        /// <param name="NeededFormatStringToRecover">Variable to place an 'Unpack'-compatible format string into.</param>
        /// <returns>A Byte array containing the objects provided in binary format.</returns>
        public static byte[] Pack(object[] items, bool LittleEndian, out string NeededFormatStringToRecover)
        {

            // make a byte list to hold the bytes of output
            List<byte> outputBytes = new List<byte>();

            // should we be flipping bits for proper endinanness?
            bool endianFlip = (LittleEndian != BitConverter.IsLittleEndian);

            // start working on the output string
            string outString = (LittleEndian == false ? ">" : "<");

            // convert each item in the objects to the representative bytes
            foreach (object o in items)
            {
                Debug.WriteLine(o.GetType());
                byte[] theseBytes = TypeAgnosticGetBytes(o);
                if (endianFlip == true)
                    theseBytes = (byte[]) theseBytes.Reverse();
                outString += GetFormatSpecifierFor(o);
                outputBytes.AddRange(theseBytes);
            }

            NeededFormatStringToRecover = outString;

            return outputBytes.ToArray();

        }

        public static byte[] Pack(object[] items)
        {
            string dummy = "";
            return Pack(items, true, out dummy);
        }
    }
}
