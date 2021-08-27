#!/usr/bin/env ruby
# Based on https://gist.github.com/macunha1/946ed32e613a8da3c7db621a9fd286d2#file-unespace-rb
# by Georgios Gousios
# MIT-licensed

require 'sequel'
require 'mysql2'
require 'cgi'

Sequel::Database.extension :pagination
DB = Sequel.connect(adapter: 'mysql2', user: '<dbuser>', password: '<password>', host: 'localhost', database: 'stackoverflow', encoding: 'utf8mb4')

table = ARGV[0].to_sym
field = ARGV[1].to_sym

lines = 0
lines_with_escapes = 0
except = 0
DB.from(table.to_sym).select(:Id, field).each_page(20000) do |page|
  page.each do |row|
    lines += 1
    text = row[field]

    next if text.nil?

    text_unescaped = CGI.unescapeHTML(text)
    begin
      if text_unescaped != text
        lines_with_escapes += 1
        DB[table].filter(:Id => row[:Id]).update(field => text_unescaped)
      end
    rescue Exception
      except += 1
    end

    print "\r #{lines} lines, #{lines_with_escapes} with escapes. Total exceptions: #{except}"
  end
end

