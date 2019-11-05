define([],function(){
    var ui = {
        type: "clean",
        rows: [
            {
                view: "form", id: "file_contents_form", complexData: true, elements: [
                    {
                        view:"text",
                        label:"Mode",
                        name:"data.mode",
                        disabled:false,
                        labelWidth:300 // TODO should not be necessary
                    },
                    { view:"text", label:"Command", name:"data.command", disabled:false},

                ]
            },
            {} // spacer
        ]
    };

	return {
		$ui: ui,
		$menu: "top:menu",
	};
});