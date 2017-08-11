#!/usr/bin/env python

import packet
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", help = "project name")
    parser.add_argument("--host", help = "host name")
    parser.add_argument("--vol", help = "volume name")
    parser.add_argument("--listplans", help = "list plans", action="store_true")
    parser.add_argument("--listprojects", help = "list projects", action="store_true")
    parser.add_argument("--listhosts", help = "list hosts", action="store_true")
    parser.add_argument("--listvols", help = "list volumes", action="store_true")
    parser.add_argument("--createvol", help = "create volumes", action="store_true")
    parser.add_argument("--createhost", help = "create new host", action="store_true")
    parser.add_argument("--deletehost", help = "delete host", action="store_true")
    parser.add_argument("--plan", help = "plan when creating host")
    parser.add_argument("--facility", help = "facility")
    parser.add_argument("--listkeys", help = "list ssh keys", action="store_true")
    parser.add_argument("--listfacility", help = "list all facilities", action="store_true")
    parser.add_argument("--listos", help = "list operating systems", action="store_true")
    parser.add_argument("--os", help = "operating systems")
    parser.add_argument("--key", help= "ssh key label")
    parser.add_argument("--attach", help="attach volume", action="store_true")
    parser.add_argument("--detach", help="detach volume", action="store_true")

    args = parser.parse_args()

    with open("apikeys") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    apikey = content[0]

    manager = packet.Manager(auth_token=apikey)

    projects = manager.list_projects()

    if args.listprojects:
        for project in projects:
            print(project.name)

    assert(len(projects) > 0)

    proj = None

    if args.project:
        for project in projects:
            if project.name == args.project:
                proj = project

    if args.listplans:
        plans = manager.list_plans()
        for plan in plans:
            print(plan)

    params = {
        'per_page': 50
    }

    if not proj:
        return

    devices = manager.list_devices(project_id=proj.id, params = params)
    host = None
    for device in devices:
        if device.hostname == args.host:
            host = device
        if args.listhosts:
            print("%s %s %s %s" % (device.hostname, device.ip_addresses[0]["address"], device.ip_addresses[2]["address"], device.state))

    vols = manager.list_volumes(project_id = proj.id)
    volume = None
    for vol in vols:
        if vol.name == args.vol:
            volume = vol
        if args.listvols:
            print("%s %dGB %s" % (vol.name, vol.size, vol.state))

    facilities = manager.list_facilities()
    for facility in facilities:
        if args.listfacility:
            print(facility.code)

    if args.listkeys:
        keys = manager.list_ssh_keys()
        for key in keys:
            print(key.label)

    if args.listos:
        oses = manager.list_operating_systems()
        for os in oses:
            print(os.slug)

    if args.deletehost:
        assert(host != None)
        host.delete()

    if args.createhost:
        assert(args.host != None)
        assert(args.facility != None)
        assert(args.plan != None)
        assert(args.os != None)
        host = manager.create_device(project_id=proj.id,
                facility = args.facility,
                hostname = args.host,
                plan=args.plan,
                operating_system=args.os)
    if args.attach:
        assert(volume != None)
        assert(host != None)
        volume.attach(host.id)
    if args.detach:
        assert(volume != None)
        volume.detach()

if __name__ == "__main__":
    main()
