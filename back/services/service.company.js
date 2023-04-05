run_script = require('../Utils/process_utils')
const { exec } = require('child_process');

class CompanyService {
  static ExportEmployFromTheName(data) {
    console.log(data);
    let yourscript = exec(`python3 /home/vietvb/Keyce/Code/linkedin-email-extractor/lee.py "${data}" "" "" 1`,
      (error, stdout, stderr) => {
        if (error !== null) {
          console.log(`exec error: ${error}`);
        }
      });
  }
}

module.exports = CompanyService;
