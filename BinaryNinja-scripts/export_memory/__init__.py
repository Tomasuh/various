from binaryninja import *


def export(bv):
    try:
        start = bv.query_metadata('start_address')
        end = bv.query_metadata('end_address')
    except KeyError:
        print "Start or end address not set"

    data = bv.read(start, end - start + 1)

    filepath_form = SaveFileNameField("Save to")
    if not get_form_input([filepath_form], "Save to"):
        return

    with open(filepath_form.result, "wb") as f:
        f.write(data)


def set_start(bv, address):
    bv.store_metadata("start_address", int(address))


def set_end(bv, address):
    bv.store_metadata("end_address", int(address))


PluginCommand.register_for_address("Set as start address for export memory",
                                   "Set as start address for export memory",
                                   set_start)
PluginCommand.register_for_address("Set as end address for export memory",
                                   "Set as end address for export memory",
                                   set_end)
PluginCommand.register("Export memory", "Export memory", export)
