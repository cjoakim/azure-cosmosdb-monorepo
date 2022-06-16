'use strict';

// Parse the out/ directory for Azure PaaS configuration values.
// Chris Joakim, Microsoft, 2020/10/26
//
// Usage:
// node parse_provisioning_output.js generate_bash_env_exports

const fs = require("fs");
const os = require("os");
const util = require('util');


class Main {

    constructor() {
        this.funct = null;
        this.env_lines = [];
    }

    execute() {
        if (process.argv.length < 3) {
            this.display_help('error: too few command-line args provided.');
            process.exit();
        }
        else {
            this.funct = process.argv[2];

            switch (this.funct) {
                case 'generate_bash_env_exports':
                    this.generate_bash_env_exports();
                    break;
                default:
                    this.display_help('undefined function: ' + this.funct);
                    break;
            }
        }
    }

    generate_bash_env_exports() {
        this.add_env_line('# Environment variables for the provisioned IoT Azure PaaS services.');
        this.add_env_line('# Set these environmnet variables for your system, such as in ~/.bash_profile')
        this.add_env_line('# Chris Joakim, Microsoft, 2020/10/26');
        this.add_env_line('# ---');

        this.wrangle_cosmos();
        this.wrangle_iothub();
        //this.wrangle_storage();

        this.add_env_line('');
        this.write_env_file();
    }

    wrangle_cosmos() {
        var create = this.read_parse_json_file('out/cosmos_sql_acct_create.json');
        var creds  = this.read_parse_json_file('out/cosmos_sql_db_connection_strings.json');
        var keys   = this.read_parse_json_file('out/cosmos_sql_db_keys.json');

        var acctName = create['name'];
        var dbName   = 'dev'; 
        var collName = 'events';
        var uri      = create['documentEndpoint'];
        var connStr  = creds['connectionStrings'][0]['connectionString'];
        var key      = keys['primaryMasterKey'];

        this.add_env_line('#')
        this.add_env_line(util.format('export AZURE_IOT_COSMOSDB_SQLDB_ACCT="%s"', acctName))
        this.add_env_line(util.format('export AZURE_IOT_COSMOSDB_SQLDB_DBNAME="%s"', dbName))
        this.add_env_line(util.format('export AZURE_IOT_COSMOSDB_SQLDB_COLLNAME="%s"', collName))
        this.add_env_line(util.format('export AZURE_IOT_COSMOSDB_SQLDB_URI="%s"', uri))
        this.add_env_line(util.format('export AZURE_IOT_COSMOSDB_SQLDB_KEY="%s"', key))
        this.add_env_line(util.format('export AZURE_IOT_COSMOSDB_SQLDB_CONN_STRING="%s"', connStr))
    }

    wrangle_iothub() {
        var hubshow     = this.read_parse_json_file('out/iothub_hub_show.json');
        var hubconnstr  = this.read_parse_json_file('out/iothub_hub_show_conn_str.json');
        var device1show = this.read_parse_json_file('out/iothub_device_id1_show.json');
        var device2show = this.read_parse_json_file('out/iothub_device_id2_show.json');
        var device1str  = this.read_parse_json_file('out/iothub_device_id1_conn_str.json');
        var device2str  = this.read_parse_json_file('out/iothub_device_id2_conn_str.json');

        var name = hubshow['name'];
        var id   = hubshow['id'];
        var hubconnstrs = hubconnstr['connectionString']; 
        var device1name    = device1show['deviceId'];
        var device2name    = device2show['deviceId'];
        var device1connstr = device1str['connectionString'];
        var device2connstr = device2str['connectionString'];

        this.add_env_line('#')
        this.add_env_line(util.format('export AZURE_IOTHUB_NAME="%s"', name))
        this.add_env_line(util.format('export AZURE_IOTHUB_RESOURCE_ID="%s"', id))
        this.add_env_line(util.format('export AZURE_IOTHUB_CONN_STR="%s"', hubconnstrs[0]))
        this.add_env_line(util.format('export AZURE_IOTHUB_DEVICE1_NAME="%s"', device1name))
        this.add_env_line(util.format('export AZURE_IOTHUB_DEVICE1_CONN_STR="%s"', device1connstr))
        this.add_env_line(util.format('export AZURE_IOTHUB_DEVICE2_NAME="%s"', device2name))
        this.add_env_line(util.format('export AZURE_IOTHUB_DEVICE2_CONN_STR="%s"', device2connstr))
    }

    wrangle_storage() {
        var create = this.read_parse_json_file('out/storage_acct_create.json');
        var showcs = this.read_parse_json_file('out/storage_acct_show_conn_str.json');
        var keys   = this.read_parse_json_file('out/storage_acct_keys.json');

        var acctName = create['name'];
        var connStr  = showcs['connectionString'];
        var key      = keys[0]['value'];

        this.add_env_line('#')
        this.add_env_line(util.format('export AZURE_IOT_STORAGE_ACCOUNT="%s"', acctName))
        this.add_env_line(util.format('export AZURE_IOT_STORAGE_KEY="%s"', key))
        this.add_env_line(util.format('export AZURE_IOT_STORAGE_CONNECTION_STRING="%s"', connStr))
    }

    read_parse_json_file(infile) {
        var txt = fs.readFileSync(infile);
        return JSON.parse(txt);
    }

    add_env_line(line) {
        this.env_lines.push(line);
    }

    write_env_file() {
        var outfile = 'bash_env_azure_iot.sh';
        fs.writeFileSync(outfile, this.env_lines.join('\n'));
        console.log(util.format('file written: %s', outfile))
    }

    display_help(error_msg) {
        if (error_msg) {
            console.log('error:');
            console.log('  ' + error_msg);
        }
        console.log('example commands:');
        console.log('  node parse_provisioning_output.js generate_bash_env_exports');
        console.log('');
    }
}

new Main().execute();
