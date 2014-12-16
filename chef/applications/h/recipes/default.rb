nodejs_npm 'coffee-script'

bash "install elasticsearch-analysis-icu" do
  code <<-EOL  
  /usr/local/elasticsearch/bin/plugin -install elasticsearch/elasticsearch-analysis-icu/2.4.1
  EOL
end

bash "restart elasticsearch" do
  code <<-EOL  
  sudo service elasticsearch restart
  EOL
end

bash "chmod" do
  code <<-EOL  
  chmod -R 777 /h
  EOL
end

template "development.ini" do
  source "development.ini.erb"
  mode 0644
  variables(
    :host => "0.0.0.0",
  )  
end
