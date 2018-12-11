require 'json'
require 'open3'

RELATIVE_DIR = 'lambda-fortran'
ABSOLUTE_DIR = '/var/task/' + RELATIVE_DIR

class CaptureRes
  def initialize(res)
    @stdout, @stderr, @status = res
  end

  def success?; @status.success?; end

  def to_h; {stdout: @stdout, stderr: @stderr, status: @status}; end
end

def response(code, status, source, extras)
  { statusCode: code,
    body: JSON.generate({status: status, source: source}.merge(extras))}
end

def lambda_handler(event:, context:)
  begin
    p event["body"]
    body = JSON.parse(event["body"])

    source = body["source"]

    File.write('/tmp/prog.f90', source)

    cmpl = CaptureRes.new(Open3.capture3(
      {'LIBRARY_PATH' => ABSOLUTE_DIR+'/g95/lib/dan-lib'},
      RELATIVE_DIR+'/g95/bin/x86_64-unknown-linux-gnu-g95 /tmp/prog.f90 -o /tmp/prog'))

    if cmpl.success?
      ex = CaptureRes.new(Open3.capture3("/tmp/prog"))

      status = ex.success? ? "success" : "execution_error"
      response(200, status, source, compilation: cmpl.to_h, execution: ex.to_h)
    else
      response(200, "compilation_error", source, compilation: cmpl.to_h)
    end
  rescue StandardError => e
      response(500, "exception", source, error: e)
  end
end
