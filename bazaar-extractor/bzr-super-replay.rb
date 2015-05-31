#!/usr/bin/ruby
#########################################################################
#
#    Copyright (C) 2011 Akretion (http://www.akretion.com). All Rights Reserved
#    Author Sebastien BEAU, Raphaël Valyi
#    Contributions : Joel Grand-Guillaume from Camptocamp
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################


STEP = 500

help_message = "
Command
bzr-super-replay path revno --module module1 module2 module3

mandatory args
path => path to the branch where the commit come from
revno => all commit will be replayed from this revision number

option
--module module1 module2 module3, -m module1 module2 module3
Only the commit for this modules will be replayed
--help
Show this message
--auto
Try to play all commit automagically ;)
--hide-merge
This option will hide all commit of merge
--hide-translation
This option will hide launchpad translation
"

oe_modules=[]
auto=false
hide_merge=false
hide_translation=false
count=0
ARGV.each do |option|
  count+=1
  if option == '--help'
    puts help_message
    exit
  elsif option == '--module' || option == "-m"
    ARGV[count..-1].each do |oe_module|
      if oe_module[0..1] == '--'
        print 'break'
        break
      else
        oe_modules << oe_module
      end
    end
  elsif option == '--auto'
    auto=true
  elsif option == '--hide-merge'
    hide_merge=true
  elsif option == '--hide-translation'
    hide_translation=true
  end
end

puts oe_modules


def index_rev(revno, commit, hide_translation, rev_lines_extended, oe_module, from_path)
  if not (hide_translation && (commit.include?('Launchpad Translations') || commit.include?('automatic translations')) || commit.strip() == "")
    rev = []
    rev_string = commit.scan(/revno.*/)[0].gsub("revno:","").strip()
    if commit.index("merge")
      rev_lines_extended += `bzr log #{from_path} -r #{rev_string.split(" ")[0]} --include-merged`
    end
    rev_string.split('.').each do |num|
      rev << num.split(" ")[0].to_i
    end
    msg = commit.split("message:")[1].strip()
    committer = commit.scan(/committer.*/)[0].gsub("committer:","").strip()
    time = commit.scan(/timestamp.*/)[0].gsub("timestamp:","").strip()[4..1000]
    puts "adding #{rev} to the rev index"
    revno[oe_module] <<  [rev, msg, committer, time]
  end
end


from_path = ARGV[0]
init_from_rev_number = ARGV[1]
puts "** SEARCHING COMMITS SINCE REV #{init_from_rev_number} **"
revno={}
current_rev = `cd #{from_path}; bzr revno`.to_i
oe_modules.each do |oe_module|
  revno[oe_module] = []
  from_rev_number = init_from_rev_number
  until_rev = from_rev_number.split('.')[0].to_i + STEP
  stop = false
  while not stop
    if until_rev > current_rev
      until_rev = current_rev
      stop = true
    end
    puts "========= searching commits from #{from_rev_number} until #{until_rev} ============="
    rev_lines = `bzr log #{from_path}/#{oe_module} -r #{from_rev_number}..#{until_rev} --include-merged`
    rev_lines_extended = ""
    rev_lines.split("------------------------------------------------------------").each do |commit|
      index_rev(revno, commit, hide_translation, rev_lines_extended, oe_module, from_path)
    end
    rev_lines_extended.split("------------------------------------------------------------").each do |commit|
      index_rev(revno, commit, hide_translation, rev_lines_extended, oe_module, from_path)
    end
    from_rev_number = until_rev
    until_rev += STEP
  end
end

rev_number = []
revno.each do | oe_module, rev_data |
  rev_number += rev_data
end

rev_number.uniq!
rev_number.sort!

original_whoami = `bzr whoami`
original_whoami.chomp!

puts "** REPLAYING REVISIONS **"
puts "#{rev_number.size} revisions to replay"
puts "hint: usually it's handy to open other terminal in the folder to fix failed replays"

`rm -rf /tmp/bzr-replay`
`mkdir /tmp/bzr-replay`

rev_number.each do |rev, message, committer, time|
  revno = rev*'.'
  puts "\nreplaying revno #{revno}"
  message += "\n(#{from_path} rev #{revno})"
  puts "commit message : #{message}"

  err = ""

  # `rm -rf *`
  `bzr whoami "#{committer}"`
  # Comment : on veut pas écraser les commit existant...
  `cd #{from_path};bzr revert --r=#{revno}`
  
  oe_modules.each do |mod|
    `cp -rf #{from_path}/#{mod} .`
  end

  current_modules = `ls`.split("\n")

  `bzr add #{current_modules.join(" ")}`
  `bzr status`
  `bzr commit -m "#{message}" --commit-time="#{time}"`
end

`bzr whoami "#{original_whoami}"`
