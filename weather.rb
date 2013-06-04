#!/usr/bin/ruby

require 'net/http'
require 'uri'

def fetchUrl(url)
	Net::HTTP.get(URI.parse(url))
end

def fetchMatches
	content = fetchUrl("http://www.wetter.info/deutschland/niedersachsen/wetter-obernkirchen/17755304")
	tempMatches = content.scan(/<p class="Tfwv(high|low) Tfwvd"><a href=".+?">(\d+?)°/)
	dateMatches = content.scan(/<span class="Tfwvdate"><a href=".+?">(\w{2}) (\d{2}.\d{2}.)/)
	{ :temperature => tempMatches, :date => dateMatches}
end

def printMatches(matches)
	matches[:date].each_with_index do |d,i|
		tempLow = matches[:temperature][i*2][1]
		tempHigh = matches[:temperature][i*2+1][1]
		puts("Datum: #{d[0]} #{d[1]}, Low: #{tempLow}, High: #{tempHigh}")
	end
end

printMatches(fetchMatches)

