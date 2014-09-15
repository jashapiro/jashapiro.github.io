# Modified from jekyll-bootstrap

require "rubygems"
require 'rake'
require 'yaml'
require 'time'

SOURCE = "."
CONFIG = {
  'layouts' => File.join(SOURCE, "_layouts"),
  'posts' => File.join(SOURCE, "_posts"),
  'post_ext' => "markdown"
}

rmd_files = Rake::FileList.new("**/*.Rmd") do |fl|
  fl.exclude(/^_.+\//) # exclude directories that start with "_"
  fl.exclude(/^scratch\//)
end

# Usage: rake post title="A Title" [date="2012-02-09"]
desc "Begin a new post in #{CONFIG['posts']}"
task :post do
  abort("rake aborted: '#{CONFIG['posts']}' directory not found.") unless FileTest.directory?(CONFIG['posts'])
  title = ENV["title"] || "new-post"
  slug = title.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
  begin
    date = (ENV['date'] ? Time.parse(ENV['date']) : Time.now).strftime('%Y-%m-%d')
  rescue Exception => e
    puts "Error - date format must be YYYY-MM-DD, please check you typed it correctly!"
    exit -1
  end
  filename = File.join(CONFIG['posts'], "#{date}-#{slug}.#{CONFIG['post_ext']}")
  if File.exist?(filename)
    abort("rake aborted!") if ask("#{filename} already exists. Do you want to overwrite?", ['y', 'n']) == 'n'
  end
  
  puts "Creating new post: #{filename}"
  open(filename, 'w') do |post|
    post.puts "---"
    post.puts "layout: post"
    post.puts "date: #{Time.now.strftime('%Y-%m-%d %k:%M:%S')}"
    post.puts "title: \"#{title.gsub(/-/,' ')}\""
    post.puts "nav: labnote"
    post.puts 'description: ""'
    post.puts "category: "
    post.puts "tags: []"
    post.puts "---"
  end
end # task :post


desc "Launch preview environment"
task :preview do
  system "bundle exec jekyll serve --watch"
end # task :preview



desc "compile markdown files"
task :knit => :markdown


task :markdown => rmd_files.ext(".markdown")
rule ".markdown" => ".Rmd" do |t|
  basedir = Dir.getwd
  Dir.chdir(File.dirname(t.source))
  source = File.basename(t.source)
  output = File.basename(t.name)
  sh "Rscript --vanilla -e 'knitr::knit(\"#{source}\", \"#{output}\")'"
  Dir.chdir(basedir)
end

desc "Rebuild Bootstrap-derived theme with lessc"
task :bootstrap do
  system "lessc _theme/shapbio.less _theme/bootstrap.css"
  system "lessc --clean-css _theme/shapbio.less _theme/bootstrap.min.css"
  system "cp _theme/bootstrap.* css/."
end # task :lessc