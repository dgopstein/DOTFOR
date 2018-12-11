require 'json'
require 'open3'

RELATIVE_DIR = 'lambda-fortran'
ABSOLUTE_DIR = '/var/task/' + RELATIVE_DIR

def lambda_handler(event:, context:)
  source = event["source"]

  File.write('/tmp/prog.f90', source)

  cmpl_out, cmpl_err, cmpl_status = Open3.capture3(
    {'LIBRARY_PATH' => ABSOLUTE_DIR+'/g95/lib/dan-lib'},
    RELATIVE_DIR+'/g95/bin/x86_64-unknown-linux-gnu-g95 /tmp/prog.f90 -o /tmp/prog')

  execution = if cmpl_status.success?
                Open3.capture3("/tmp/prog")
              else
                ['','','']
              end

  { statusCode: 200,
    body: JSON.generate(compilation: [cmpl_out, cmpl_err, cmpl_status], execution: execution) }
end
