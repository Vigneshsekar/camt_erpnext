frappe.ui.form.on("Bank Statement Import", {
    custom_convert_xml_to_csv(frm,cdt,cdn){
        /*	console.log(frm.doc.camt_xml_file)
            frappe.call({
                            method: "erpnext.accounts.doctype.bank_statement_import.bank_statement_import.convert_xml_to_csv",
                            args: {
                    xml_file: frm.doc.camt_xml_file
                            },
                            callback: function (r) {
                                    console.log(r.message);
                    frm.set_value('import_file',r.message)
                    frm.refresh_field('import_file')
                            }
                    });*/
             console.log(frm.doc.camt_xml_file)
                    frappe.call({
                            method: "camt_erpnext.camt_erpnext.bank_statement_import.convert_xml_to_csv",
                            args: {
                                    file: frm.doc.custom_camt_xml_file
                                      
                },
                            callback: function (r) {
                                    console.log("this is the original path "+ r.message);
                                    var value = r.message
                                    var value_path = value.split('files/')
                                    console.log("this is value path "+ value_path)
                
                    
                    
                    let imagefile = new FormData()
                    imagefile.append('file_url','/files/'+value_path[1])
                        console.log(imagefile)
                    //imagefile.append('doctype',"Bank Statement Import")
                    //imagefile.append('docname',frm.doc.name)
                           fetch('/api/method/upload_file',{
                        headers:{
                            
                            'X-Frappe-CSRF-Token':frappe.csrf_token
                        },
                        method:'POST',
                                            body:imagefile,
    
                    })
                    .then(res=>res.json())
                    .then(data=>{
                        console.log(data)
                            console.log(data.message.file_name)	
                        $.ajax({
                                            url:`/api/resource/Bank Statement Import/${frm.doc.name}`,
                                            type:'PUT',
                                            headers:{
                                            'Content-Type':'application/json',
                                            'X-Frappe-CSRF-Token':frappe.csrf_token
                                            },
                                            data:JSON.stringify({import_file:data.message.file_url}),
                                            success:function(data){
                                                    return data
                                            },
                                            error:function(data){
                                                    return data
                                            }
                                    })
                                   .then(res=>res.json())
                                            .then(dataa=>{
                                                console.log(dataa)
                                            })
                    })
                    /*let imgres = fetch('http://192.168.1.107:8585/api/method/upload_file',{
                        headers:{
                            'X-Frappe-CSRF-Token':frappe.csrf_token
                        },
                        method:"PUT",
                        data:JSON.stringify({import_file:"files/"+value_path[1]}),
                    
                    }) 
                        .then(res=>res.json())
                        .then(data=>{
                                                console.log(data)
                        })*/
                    
                     
    
                                      
                    /*$.ajax({
                        url:`/api/resource/Bank Statement Import/${frm.doc.name}`,
                        type:'PUT',
                        headres:{
                        'Content-Type':'application/json',
                        'X-Frappe-CSRF-Token':frappe.csrf_token
                        },
                        data:JSON.stringify({import_file:'files/'+value_path[1]}),
                        //success:function(data){
                            return data
                        },
                        //error:function(data){
                            return data
                        }
                    })
                    .then(res=>res.json())
                                            .then(dataa=>{
                                                console.log(dataa)
                                            })*/
                                    //frappe.model.set_value(cdt,cdn,'import_file',"/files/"+value_path[1])
                                    //frm.refresh_field('import_file')
                                    
                            }
                    });
                    frm.save();
                    //window.location.reload()
                    //frm.refresh()
    },
    });

