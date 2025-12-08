import time
import logging
from simplexMotor import SimplexMotor  # Import your custom class

# === Configuration Constants ===
# Modify these parameters according to your hardware setup
PORT = 'COM3'
SLAVE_ID = 1
BAUDRATE = 57600

def setup_global_logging():
    """
    Configures the root logger for the entire application.
    This acts as the master switch for all log outputs.
    """
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG to capture detailed hardware logs
        format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Suppress verbose logs from third-party libraries (e.g., pymodbus)
    # keeping only warnings and errors to reduce console noise.
    logging.getLogger("pymodbus").setLevel(logging.WARNING)

def main():
    # 1. Initialize Logging System
    setup_global_logging()
    
    # Create a specific logger for the main controller logic
    # This helps distinguish high-level application logs from low-level driver logs
    logger = logging.getLogger("MainController")
    logger.info("System Starting...")

    # 2. Instantiate the Motor Object
    # debug=True ensures we see the hex dumps from the driver
    motor = SimplexMotor(port=PORT, baudrate=BAUDRATE, slave_id=SLAVE_ID, debug=True)

    try:
        # 3. Establish Connection
        motor.connect()
        
        # 4. Initial Configuration
        # Example: Set resolution to 16384 cpr (Mode 2)
        # This will trigger an INFO log if the setting actually changes
        logger.info("Initializing Motor Settings...")
        motor.set_position_resolution(mode=2)
        
        logger.info("Starting Control Loop. Press Ctrl+C to stop.")
        
        # 5. Main Control Loop
        while True:
            # Wrap hardware interactions in a try-block to prevent the loop 
            # from crashing due to transient communication errors.
            try:
                # Fetch telemetry data
                pos_deg = motor.get_position()
                speed = motor.get_speed()
                torque_max = motor.get_torque_max()
                
                # Display status on console (User Interface)
                # Using print() here allows for a clean dashboard view, 
                # separate from the scrolling logs.
                print(f">>> STATUS | Pos: {pos_deg:8.2f} deg | Speed: {speed:8.2f} deg/s | MaxTorque: {torque_max:.3f} Nm")
                
            except RuntimeError as e:
                # Log the error but keep the loop running (retry mechanism)
                logger.warning(f"Communication error in loop: {e}")
            
            # Control loop frequency (e.g., 1Hz)
            time.sleep(1.0)

    except KeyboardInterrupt:
        # Handle graceful shutdown when user presses Ctrl+C
        logger.info("User requested stop (KeyboardInterrupt).")
        
    except Exception as e:
        # Catch-all for unexpected crashes to ensure we see the error cause
        logger.critical(f"System crashed due to unhandled exception: {e}", exc_info=True)
        
    finally:
        # 6. Safety Shutdown
        # Always ensure the connection is closed, even if errors occurred.
        logger.info("System Shutting Down...")
        motor.close()

if __name__ == "__main__":
    main()