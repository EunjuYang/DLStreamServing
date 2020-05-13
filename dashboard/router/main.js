module.exports = function(app, fs, upload, grpc, client, mongoose)
{
    var models = [];
    var target_model = "none";
    var amis = ["ami0", "ami1", "ami2"];

    var mongo_connet_manager = {};

//    fs.readFile( __dirname + "/../data/model_state.json", 'utf8', function (err, data) {
//        var models_json = JSON.parse(data);

//        for (var key in models_json) {
//            models.push(models_json[key])
//        }
//    });

    app.get('/',function(req,res){

        var model_count = {"deploy": 0, "pause": 0};
        for(var i=0, item; item=models[i]; i++) {
            if (item['model_state']=="deploy") {
                model_count["deploy"] += 1
            } else {
                model_count["pause"] += 1
            }
        }

        res.render('index', {
             title: "home",
             model_count: model_count
        })
    });

    app.get('/main/home',function(req,res){

        var model_count = {"deploy": 0, "pause": 0};
        for(var i=0, item; item=models[i]; i++) {
            if (item['model_state']=="deploy") {
                model_count["deploy"] += 1
            } else {
                model_count["pause"] += 1
            }
        }

        res.render('index', {
            title: "home",
            model_count: model_count
        })
    });

    // /main/model_management 링크 클리시 모델 관리 화면으로 이동
    app.get('/main/model_management', function(req, res){

// Todo...
// Todo -> gRPC function - rpc get_deployed_model(null) returns (ModelList) {}
// Todo -> server(model repo)에서 관리하고 있는 모델 리스트 전송 받기
        // 이후, models 및 model_count 업데이트

        console.log('******************** gRPC get_deployed_model start');

        client.get_deployed_model({}, function(err, response) {
            models = []
            if(!err){
                console.log('success fetched model lists');
                console.log(response);

                for (var i=0; i < response["model"].length; i++) {
                    var model = {
                        'amis': [],
                        'input_format': {},
                        'online_param': {}
                    };
                    model['model_name'] = response["model"][i]['name']
                    model['amis'] = response["model"][i]['amis']
                    model['input_format'] = response["model"][i]['input_fmt']
                    model['UUID'] = response["model"][i]['UUID']
                    model['create_time'] = response["model"][i]['create_time']
                    model['update_time'] = response["model"][i]['update_time']
                    model['is_online_train'] = response["model"][i]['is_online_train']
                    model['online_param'] = response["model"][i]['online_param']
                    console.log(model)
                    models.push(model)
                }
            } else {
                console.error(err);
            }
        });

        res.render('model_management', {
            title: "model_management",
            models: models
        })
    });

    app.post('/main/model_management', upload.single('model_object'), function(req, res){
        var moment = require('moment');

        // 사용자가 입력한 배포할 모델 정보 파싱
        var model = {
            'amis': [],
            'input_format': {},
            'online_param': {}
        };
        // common input params
        model['is_online_train'] = (req.body.is_online_train == "true");
        model['model_name'] = req.body.model_name;
        model['UUID'] = guid();
        model['create_time'] = moment().format('YYYY-MM-DD HH:mm:ss');
        model['update_time'] = moment().format('YYYY-MM-DD HH:mm:ss');
        model['model_object'] =  __dirname + "/../" + req.file.path;
        model['is_adaptive'] = (req.body.is_adaptive == "true");
        model['input_format']['look_back_win_size'] = parseInt(req.body.look_back_win_size);
        model['input_format']['input_shift_step'] = parseInt(req.body.input_shift_step);
        model['model_state'] = "deploy";

        // is online learning
        if (req.body.is_online_train == "true") {
            model['amis'] = req.body.ami_list_online.split("   ");
            model['amis'].pop();
            model['input_format']['look_forward_step'] = parseInt(req.body.look_forward_step);
            model['input_format']['look_forward_win_size'] = parseInt(req.body.look_forward_win_size);
            model['online_param']['online_method'] = req.body.online_method;
            model['online_param']['batch_size'] = parseInt(req.body.batch_size);

            // is cont online method
            if (req.body.online_method == "cont") {
                model['online_param']['memory_method'] = req.body.memory_method;
                model['online_param']['is_schedule'] = (req.body.is_schedule == "true");
                model['online_param']['episodic_mem_size'] = parseInt(req.body.episodic_mem_size);
            }
        } else {
            model['amis'] = req.body.ami_list_without_online.split("   ");
            model['amis'].pop();
        }
        console.log(model);

        // 자체 모델 관리 리스트에 업데이트
        models.push(model);

// Todo...
// Todo -> gRPC function - rpc set_deploy_model(stream Model) returns (Reply) {}
// Todo -> server에 배포할 모델 정보 전송 하기

        console.log('******************** gRPC set_deploy_model start');

        let call = client.set_deploy_model(function (error, response) {
            console.log("Reports successfully generated");
            console.log(response);
        });

        fs.readFile(model['model_object'], (err, data) => {
            if (err) throw err;
            call.write({
                name: model['model_name'],
                amis: {ami_id: model['amis']},
                buffer: data,
                input_fmt: {
                    look_back_win_size: model['input_format']['look_back_win_size'],
                    input_shift_step: model['input_format']['input_shift_step'],
                    look_forward_step: model['input_format']['look_forward_step'],
                    look_forward_win_size: model['input_format']['look_forward_win_size']
                },
                is_online_train: model['is_online_train'],
                update_time: model['update_time'],
                create_time: model['create_time'],
                UUID: model['UUID'],
                online_param: model['online_param']
            });

        call.end();
        });


        res.render('model_management', {
            title: "model_management",
            models: models
        })
    });

    // /main/input_model 화면에서 Search AMI List 버튼 클릭시 /main/ami_list_select_page 화면으로 이동
    app.get('/main/online_ami_list_select_page.html', function(req, res){

        res.render('online_ami_list_select_page', {
            title: "online_ami_list_select_page",
            amis: amis
        })
    });

    app.get('/main/without_online_ami_list_select_page.html', function(req, res){

        res.render('without_online_ami_list_select_page', {
            title: "without_online_ami_list_select_page",
            amis: amis
        })
    });

    app.post('/main/delete_model', function(req, res){

        for(var i=0, item; item=models[i]; i++) {
            if (item['UUID']==req.body.delete_model_uuid) {
                target_model = item
            }
        }
        console.log(target_model['model_name']);
// Todo...
        //
        console.log('******************** gRPC stop_deployment');
        let call = client.stop_deployment(function (error, response) {
            console.log("Reports successfully generated");
            console.log(response);
        });

        call.write({name: target_model['model_name']});
        call.end();

        res.render('model_management', {
            title: "model_management",
            models: models
        })
    });

    // /main/management 화면에서 Deploy Model 버튼 클릭시 /main/input_model 화면으로 이동
    app.get('/main/input_model', function(req, res){
        res.render('input_model_form', {
            title: "input_model_form"
        })

// Todo -> gRPC function - rpc get_ami_list(null) returns (AMIList) {}
// Todo...
        // prefix 변수로 관리

        amis=[];
        console.log('******************** gRPC get_ami_list start');

        client.get_ami_list({}, function(err, response) {
            if(!err){
                console.log('success fetched AMI lists');
                console.log(response);
                for (var i=0; i < response['ami_id'].length; i++){
                    amis.push((response['ami_id'][i]).split('.')[1])
                }
                console.log(amis);
            } else{
                console.error(err);
            }
        });
    });

    app.post('/main/deploy_model_info', function(req, res){

        for(var i=0, item; item=models[i]; i++) {
            if (item['UUID']==req.body.deploy_model_uuid) {
                target_model = item
                break
            }
        }

        var txt = "";
        for (var j = 0; j < target_model['amis'].length; j++) {
            txt = txt + target_model['amis'][j] + " ";
        }

        target_model['ami'] = txt

        res.render('deploy_model_info', {
            title: "deploy_model_info",
            model: target_model
        })
    });

    app.post('/main/restart_model', function(req, res){

        for(var i=0, item; item=models[i]; i++) {
            if (item['UUID']==req.body.restart_model_uuid) {
                target_model = item
                models[i]['model_state'] = "deploy"
                target_model['model_state'] = "deploy"
                break
            }
        }

// Todo...
        // rpc restart_online_train(ModelName) returns (Reply) {}
        // pause 상태 모델 id 전송해서 deploy restart 전송

        res.render('model_management', {
            title: "model_management",
            models: models
        })
    });

    app.post('/main/pause_model', function(req, res){

        for(var i=0, item; item=models[i]; i++) {
            if (item['UUID']==req.body.pause_model_uuid) {
                target_model = item
                models[i]['model_state'] = "pause"
                target_model['model_state'] = "pause"
                break
            }
        }

// Todo...
        // rpc stop_online_train(ModelName) returns (Reply) {}
        // deploy 상태 모델 id 전송해서 deploy stop 전송

        res.render('model_management', {
            title: "model_management",
            models: models
        })
    });

    app.post('/main/inference', function(req, res){
        for(var i=0, item; item=models[i]; i++) {
            if (item['UUID']==req.body.inference_model_uuid) {
                target_model = item
                break
            }
        }

        let Schema = mongoose.Schema;
        let inferenceSchema = new Schema({
            amiid: Number,
            pred: [Number],
            true: [Number],
            timestamp: Number
        }, {
            collection: target_model['model_name']
        });
        let Inference = mongoose.model(target_model['model_name'], inferenceSchema);

        var inference_result = {};
        for (var j = 0; j < target_model.amis.ami_id.length; j++) {
            var dict = {}
            dict['pred_v'] = []
            dict['true_v'] = []
            inference_result[target_model.amis.ami_id[j]] = dict;
        }

        console.log('target_model')
        console.log(target_model)
        console.log(inference_result)

        Inference.find(function(err, response){
            if(err) return res.status(500).send({error: 'database failure'});

            var count=0;
            if (response.length < 3000){
                count = response.length
            } else {
                count = 3000
            }
            console.log(response)
            console.log(inference_result)
            console.log('db count is ' + count)
            for (var i = 0; i < count; i++) {
                for (var key in inference_result){
                    var amiid = response[i].amiid
                    if (parseInt(key.split('i')[1]) == amiid) {
                        inference_result[key]['pred_v'] = inference_result[key]['pred_v'].concat(response[i]['pred'])
                        inference_result[key]['true_v'] = inference_result[key]['true_v'].concat(response[i]['true'])
                    }
                }
            }

            res.render('inference', {
                title: "inference",
                model: target_model,
                result: inference_result
            })
        })
        mongoose.deleteModel(target_model['model_name'])
    });

    function guid() {
        function s4() {
            return ((1 + Math.random()) * 0x10000 | 0).toString(16).substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
    }
}
