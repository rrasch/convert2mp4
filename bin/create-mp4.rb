#!/usr/bin/env ruby

require 'logger'
require 'open3'
require 'optparse'

def do_cmd(cmd, log)
  log.debug "Running '#{cmd}'"
  output, status = Open3.capture2e(cmd)
  log.debug output
  if ! status.exitstatus.zero?
    log.error "#{cmd} exited with status #{status.exitstatus}"
    exit 1
  end
  return output
end

options = {
  :profile => "movie-scenes",
  :quiet => false,
}

OptionParser.new do |opts|

  opts.banner = "Usage: #{$0} [options] [wip_ids]... "

  opts.on('-r', '--rstar-dir DIRECTORY', 'R* directory for collection') do |r|
    options[:rstar_dir] = r
  end
  
  opts.on('-p', '--profile PROFILE', 'Video encoding profile') do |p|
    options[:profile] = p
  end

  opts.on('-e', '--extra-args ARGUMENTS', 'Extra cmd line arguments') do |e|
    options[:extra_args] = e
  end

  opts.on('-q', '--quiet', 'Suppress debugging messages') do
    options[:quiet] = true
  end

  opts.on('-h', '--help', 'Print help message') do
    puts opts
    exit
  end

end.parse!

logger = Logger.new($stderr)
if options[:quiet]
  logger.level = Logger::INFO
end

if !options[:rstar_dir]
  abort "You must specify an R* directory."
elsif !File.directory?(options[:rstar_dir])
  abort "R* directory '#{options[:rstar_dir]}' doesn't exist."
end

wip_dir = options[:rstar_dir] + "/wip/se"
logger.debug "wip_dir: #{wip_dir}"

ids = []
if ARGV.size > 0
  ids = ARGV
else
  ids = Dir.glob("#{wip_dir}/*").map{ |d| File.basename(d) }.sort
end

ids.each do |id|
  data_dir = "#{wip_dir}/#{id}/data"
  logger.debug "data_dir: #{data_dir}"
  aux_dir  = "#{wip_dir}/#{id}/aux"
  logger.debug "aux_dir:  #{aux_dir}"
  log_file = "#{aux_dir}/transcode_#{id}.log"

  input_files = Dir.glob("#{data_dir}/*_d.{avi,mkv,mov,mp4}")
  input_files.each do |input_file|
    logger.debug "input_file: #{input_file}"
    basename = File.basename(input_file, ".*")
    basename.sub!(/_d$/, '')
    output_prefix = "#{aux_dir}/#{basename}"
    cmd = "convert2mp4"
    if options[:quiet]
      cmd << " -q"
    end
    cmd << " --profiles_path profiles-#{options[:profile]}.xml"\
           " --path_tmpdir /content/prod/rstar/tmp"\
           " #{options[:extra_args]} #{input_file} #{output_prefix}"\
           " >> #{log_file} 2>&1"
    do_cmd(cmd, logger)
    cs_file = "#{aux_dir}/#{basename}_contact_sheet.jpg"
    if !File.file?(cs_file)
      do_cmd("vcs #{input_file} -o #{cs_file} >> #{log_file} 2>&1", logger)
    end
  end
end

