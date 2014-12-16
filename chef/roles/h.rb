name "h"
description "Hypothes.is h server"

run_list(
  "recipe[build-essential]",
  "recipe[apt]",  
  "recipe[git]",
  "recipe[nodejs]",
  "recipe[elasticsearch]",
  "recipe[java]",
  "recipe[python]",
  "recipe[rvm::system]",
  "recipe[h]"
)

default_attributes(

  :rvm => {
    :rubies => ["ruby-1.9.3-p125"],
    :default_ruby => "ruby-1.9.3-p125",    
    :gems => {
      'ruby-1.9.3-p125' => [
        {'name' => 'sass'},
        {'name' => 'compass'}
      ]     
    }   
  },

  'elasticsearch' => {
    :version => "1.4.1"
  },

  'nodejs' => {
    :install_method => "source"      
  },

  'java' => {
    :install_flavor => 'oracle',
    :jdk_version => '7',
    :oracle => { :accept_oracle_download_terms => true }
  }

)