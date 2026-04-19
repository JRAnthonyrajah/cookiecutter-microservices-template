/**
 * {{ cookiecutter.service_name }}
 * Entry point for the Node.js service
 */

const logger = {
  info: (msg) => console.log(`[INFO] ${msg}`),
  error: (msg) => console.error(`[ERROR] ${msg}`),
};

async function main() {
  try {
    logger.info('Starting {{ cookiecutter.service_name }}');
    // TODO: Implement service logic
    logger.info('Service is running');
  } catch (error) {
    logger.error(`Failed to start service: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };
