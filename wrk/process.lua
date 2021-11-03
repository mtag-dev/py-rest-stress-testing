-- Module instantiation
local cjson = require "cjson"
local cjson2 = cjson.new()
local cjson_safe = require "cjson.safe"

-- Read framework and fixture configuration
local framework = os.getenv("FRAMEWORK")
local fixture_path = os.getenv("FIXTURE")
local filename = os.getenv("FILENAME")

-- Load URL paths from the file
function load_fixture(file)
  local f=io.open(file,"r")
  local content
  if f~=nil then
    content = f:read("*all")
    io.close(f)
    data = cjson.decode(content)
    if data.request.payload~=nil then
      data.request.payload = cjson.encode(data.request.payload)
    end
    return data
  else
    print("Fixture file not found: " .. file )
    os.exit()
  end
end

-- Load URL requests from file
fixture = load_fixture(fixture_path)

function interp(s, tab)
  return (s:gsub('($%b{})', function(w) return tab[w:sub(3, -2)] or w end))
end

-- Initialize counter
counter = 1

request = function()
  counter = counter + 1  -- Increment dynamic counter
  return wrk.format(
      fixture.method,
      interp(fixture.request.path, { dynamic = counter }),
      fixture.request.headers,
      fixture.request.body
    )
end


done = function(summary, latency, requests)
    file = assert(io.open(filename, "a"))
    file.write(
        file,
        string.format(
            "%s,%d,%.2f,%.2f,%.2f,%.2f,%d,%d,%d\n",
            framework,
            summary.requests,
            latency:percentile(50) / 1000,
            latency:percentile(75) / 1000,
            latency:percentile(90) / 1000,
            latency.mean / 1000,
            summary.errors.status,
            summary.errors.read,
            summary.errors.timeout
            ));
    file.close()
end
