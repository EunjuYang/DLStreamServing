//module.exports = function(app, fs, upload, grpc, client, request, mongoose)
module.exports = function(app, fs, upload, grpc, client, request, mongoose, instanceTrain, instanceInfer)
{
    var models = [];
    var target_model = "none";
    var amis = ["ami0", "ami1", "ami2"];
    var select_model = "none";

    var mongo_connet_manager = {};

    var db_data_sync = {};

    app.get('/',function(req,res){

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
                    model['create_time'] = new Date(parseInt(response["model"][i]['create_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
                    model['update_time'] = new Date(parseInt(response["model"][i]['update_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
                    model['is_online_train'] = response["model"][i]['is_online_train']
                    model['online_param'] = response["model"][i]['online_param']
                    console.log(model)
                    models.push(model)
                }
            } else {
                console.error(err);
            }
        });

        var model_count = {"deploy": 0, "pause": 0};
        model_count["deploy"] = models.length

        res.render('index', {
             title: "home",
             model_count: model_count
        })
    });

    app.get('/main/home',function(req,res){

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
                    model['create_time'] = new Date(parseInt(response["model"][i]['create_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
                    model['update_time'] = new Date(parseInt(response["model"][i]['update_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
                    model['is_online_train'] = response["model"][i]['is_online_train']
                    model['online_param'] = response["model"][i]['online_param']
                    console.log(model)
                    models.push(model)
                }
            } else {
                console.error(err);
            }
        });

        var model_count = {"deploy": 0, "pause": 0};
        model_count["deploy"] = models.length

        res.render('index', {
            title: "home",
            model_count: model_count
        })
    });

    // /main/model_management 링크 클리시 모델 관리 화면으로 이동
    app.get('/main/model_management', function(req, res){

// Todo -> gRPC function - rpc get_deployed_model(null) returns (ModelList) {}
// Todo -> server(model repo)에서 관리하고 있는 모델 리스트 전송 받기

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
                    model['create_time'] = new Date(parseInt(response["model"][i]['create_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
                    model['update_time'] = new Date(parseInt(response["model"][i]['update_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
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
                    model['create_time'] = new Date(parseInt(response["model"][i]['create_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
                    model['update_time'] = new Date(parseInt(response["model"][i]['update_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
                    model['is_online_train'] = response["model"][i]['is_online_train']
                    model['online_param'] = response["model"][i]['online_param']
                    console.log(model)
                    models.push(model)
                }
            } else {
                console.error(err);
            }
        });
        console.log(models)

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
        client.stop_deployment({name: target_model['model_name']}, function (error, response) {
            if(!error){
                console.log('Model is deleted Successfully')
            }
            else{
                console.error(error)
            }
        })

        if (select_model.model_name == target_model.model_name){
            select_model = "none";
        }

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
                    model['create_time'] = new Date(parseInt(response["model"][i]['create_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
                    model['update_time'] = new Date(parseInt(response["model"][i]['update_time'])*1000).toISOString().replace(/T/, ' ').replace(/Z/, '')
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
                target_model = item;
                select_model = item;
                break
            }
        }
        console.log(target_model['amis']);
        var txt = "";
        for (var j = 0; j < target_model['amis']['ami_id'].length; j++) {
            txt = txt + target_model['amis']['ami_id'][j] + " ";
        }

        target_model['ami'] = txt

        res.render('deploy_model_info', {
            title: "deploy_model_info",
            model: target_model
        })
    });

    app.post('/main/inference', function(req, res){

        for(var i=0, item; item=models[i]; i++) {
            if (item['UUID']==req.body.inference_model_uuid) {
                target_model = item;
                select_model = item;
                break
            }
        }

        console.log('target_model')
        console.log(target_model)

        var Inference;
        console.log("11111. instanceInfer Info-------")
        console.log(instanceInfer);
        while (1) {
            if (target_model['model_name'] in instanceInfer.models) {
                instanceInfer.deleteModel(target_model['model_name'])
            } else {
                console.log("Mondb Connection State --- Not Connected")
                var Schema = instanceInfer.Schema;
                var inferenceSchema = new mongoose.Schema({
                    amiid: Number,
                    pred: [Number],
                    true: [Number],
                    timestamp: Date,
                    loss: Number,
                    average_loss: Number,
                    updated_at_inferencedl: Date
                }, {
                    collection: target_model['model_name']
                });
        //let Inference = mongoose.model(target_model['model_name'], inferenceSchema);
                Inference = instanceInfer.model(target_model['model_name'], inferenceSchema);
                console.log("Mondb Connection State --- Connected Success")
                break;
            }
        }

        console.log("222222. instanceInfer Info-------")
        console.log(Object.keys(instanceInfer.models));

        var updated_time = [];
        var max_value = [0, 0, 0, 0];

        var inference_result = {};
        for (var j = 0; j < target_model.amis.ami_id.length; j++) {
            var dict = {}
            dict['pred_v'] = []
            dict['true_v'] = []
            dict['time'] = []
            dict['loss'] = []
            dict['average_loss'] = []
            inference_result[target_model.amis.ami_id[j]] = dict;
        }

        console.log(Inference)

        Inference.find(function(err, response){
            if(err) return res.status(500).send({error: 'database failure'});

            var count=0;
            count = response.length
            console.log(inference_result)
            console.log(response)
            console.log('db count is ' + count)
            for (var i = 0; i < count; i++) {
                if (typeof response[i]['pred'] !== 'undefined' && response[i]['pred'].length > 0){
                    for (var key in inference_result){
                        var amiid = response[i].amiid
                        if (parseInt(key.split('i')[1]) == amiid) {
                            inference_result[key]['pred_v'] = inference_result[key]['pred_v'].concat(response[i]['pred']);
                            inference_result[key]['true_v'] = inference_result[key]['true_v'].concat(response[i]['true']);
                            var time = new Date(response[i]['timestamp']).toISOString().replace(/T/, ' ').replace(/Z/, '');
                            for (var j = 0; j < response[i]['pred'].length; j++) {
                                inference_result[key]['loss'] = inference_result[key]['loss'].concat(response[i]['loss'])
                                inference_result[key]['average_loss'] = inference_result[key]['average_loss'].concat(response[i]['average_loss'])
                                inference_result[key]['time'].push(time);
                            }
                        }
                    }
                } else {
                    for (var key in inference_result){
                        inference_result[key]['pred_v'] = inference_result[key]['pred_v'].concat([-1]);
                        inference_result[key]['true_v'] = inference_result[key]['true_v'].concat([-1]);
                        inference_result[key]['time'].push(new Date(response[i]['updated_at_inferencedl']).toISOString().replace(/T/, ' ').replace(/Z/, ''));
                        inference_result[key]['loss'] = inference_result[key]['loss'].concat([-1]);
                        inference_result[key]['average_loss'] = inference_result[key]['average_loss'].concat([-1]);
                        updated_time.push(new Date(response[i]['updated_at_inferencedl']).toISOString().replace(/T/, ' ').replace(/Z/, ''));
                    }
                }
            }

            for (var key in inference_result){
                
                if (Math.max.apply(Math, inference_result[key]['true_v']) > max_value[1]) {
                    max_value[1] = Math.max.apply(Math, inference_result[key]['true_v']);
                }
                if (Math.max.apply(Math, inference_result[key]['pred_v']) > max_value[1]) {
                    max_value[1] = Math.max.apply(Math, inference_result[key]['pred_v']);
                }
                if (Math.max.apply(Math, inference_result[key]['loss']) > max_value[2]) {
                    max_value[2] = Math.max.apply(Math, inference_result[key]['loss']);
                }
                if (Math.max.apply(Math, inference_result[key]['average_loss']) > max_value[3]) {
                    max_value[3] = Math.max.apply(Math, inference_result[key]['average_loss']);
                }
            }
            max_value[0] = count;

            console.log(inference_result);
            console.log(updated_time);

            res.render('inference', {
                title: "inference",
                model: target_model,
                result: inference_result,
                updated_time: updated_time,
                metadata: max_value
            })
        })
        //mongoose.deleteModel(target_model['model_name'])
        instanceInfer.deleteModel(target_model['model_name'])
    });

    app.post('/main/training', function(req, res){

        for(var i=0, item; item=models[i]; i++) {
            if (item['UUID']==req.body.training_model_uuid) {
                target_model = item;
                select_model = item;
                break
            }
        }

        var Training;
        console.log("111111. instanceTrain Info-------")
        console.log(instanceTrain);
        while (1) {
            if (target_model['model_name'] in instanceTrain.models) {
                instanceTrain.deleteModel(target_model['model_name'])
            } else {
                console.log("Mongodb Connection State --- Not Connected")
                var Schema = instanceTrain.Schema;
                var trainingSchema = new mongoose.Schema({
                    amiid: Number,
                    pred: [Number],
                    true: [Number],
                    loss: [Number],
                    timestamp: Date,
                    update_at_onlinedl: Date
                }, {
                    collection: target_model['model_name']
                });
                Training = instanceTrain.model(target_model['model_name'], trainingSchema);
                console.log("Mongodb Connection State --- Connected Success")
                break;
            }
        }
        console.log("222222. instanceTrain Info-------")
        console.log(Object.keys(instanceTrain.models));

        var max_value = [0, 0, 0];

        var training_result = {};
        for (var j = 0; j < target_model.amis.ami_id.length; j++) {
            var dict = {}
            dict['pred_v'] = []
            dict['true_v'] = []
            dict['loss'] = []
            dict['time'] = []
            training_result[target_model.amis.ami_id[j]] = dict;
        }

        console.log('target_model')
        console.log(target_model)

        Training.find(function(err, response){
            if(err) return res.status(500).send({error: 'database failure'});

            var count = 0;
            count = response.length
            console.log(training_result)
            console.log('db count is ' + count)
            for (var i = 0; i < count; i++) {
                if (typeof response[i]['pred'] !== 'undefined' && response[i]['pred'].length > 0){
                    for (var key in training_result){
                        var amiid = response[i].amiid
                        if (parseInt(key.split('i')[1]) == amiid) {
                            training_result[key]['pred_v'] = training_result[key]['pred_v'].concat(response[i]['pred'])
                            training_result[key]['true_v'] = training_result[key]['true_v'].concat(response[i]['true'])
                            var time = new Date(response[i]['timestamp']).toISOString().replace(/T/, ' ').replace(/Z/, '');
                            for (var j = 0; j < response[i]['pred'].length; j++) {
                                training_result[key]['loss'] = training_result[key]['loss'].concat(response[i]['loss'])
                                training_result[key]['time'].push(time);
                            }
                        }
                    }
                } else {
                    for (var key in training_result){
                        training_result[key]['pred_v'] = training_result[key]['pred_v'].concat([-1]);
                        training_result[key]['true_v'] = training_result[key]['true_v'].concat([-1]);
                        training_result[key]['loss'] = training_result[key]['loss'].concat([-1]);
                        training_result[key]['time'].push(new Date(response[i]['update_at_onlinedl']).toISOString().replace(/T/, ' ').replace(/Z/, ''));
                    }
                }
            }
            for (var key in training_result){
                if (Math.max.apply(Math, training_result[key]['true_v']) > max_value[1]) {
                    max_value[1] = Math.max.apply(Math, training_result[key]['true_v']);
                }
                if (Math.max.apply(Math, training_result[key]['pred_v']) > max_value[1]) {
                    max_value[1] = Math.max.apply(Math, training_result[key]['pred_v']);
                }
                if (Math.max.apply(Math, training_result[key]['loss']) > max_value[2]) {
                    max_value[2] = Math.max.apply(Math, training_result[key]['loss']);
                }
            }
            max_value[0] = count;

            console.log(training_result);

            res.render('training', {
                title: "training",
                model: target_model,
                result: training_result,
                metadata: max_value
            })
        })
        //mongoose.deleteModel(target_model['model_name'])
        instanceTrain.deleteModel(target_model['model_name'])
    });

    app.get('/main/inference/append_ami', function(req, res) {
        var model_name = req.query.model_name;
        var max_value = req.query.metadata;
        var origin_count = req.query.db;

        for(var i=0, item; item=models[i]; i++) {
            if (item['model_name']==model_name) {
                target_model = item;
                break
            }
        }

        var Inference;
        console.log("11111. instanceInfer Info-------")
        console.log(instanceInfer);
        while (1) {
            if (target_model['model_name'] in instanceInfer.models) {
                instanceInfer.deleteModel(target_model['model_name'])
            } else {
                console.log("Mondb Connection State --- Not Connected")
                var Schema = instanceInfer.Schema;
                var inferenceSchema = new mongoose.Schema({
                    amiid: Number,
                    pred: [Number],
                    true: [Number],
                    timestamp: Date,
                    loss: Number,
                    average_loss: Number,
                    updated_at_inferencedl: Date
                }, {
                    collection: target_model['model_name']
                });
        //let Inference = mongoose.model(target_model['model_name'], inferenceSchema);
                Inference = instanceInfer.model(target_model['model_name'], inferenceSchema);
                console.log("Mondb Connection State --- Connected Success")
                break;
            }
        }
        console.log("222222. instanceInfer Info-------")
        console.log(Object.keys(instanceInfer.models));

        var updated_time = [];
        var inference_result = {};
        for (var j = 0; j < target_model.amis.ami_id.length; j++) {
            var dict = {}
            dict['pred_v'] = []
            dict['true_v'] = []
            dict['time'] = []
            dict['loss'] = []
            dict['average_loss'] = []
            inference_result[target_model.amis.ami_id[j]] = dict;
        }

        console.log(Inference)

        Inference.find(function(err, response){
            if(err) return res.status(500).send({error: 'database failure'});

            var count=0;
            var new_response = response.slice(origin_count);
            count = new_response.length
            console.log(inference_result)
            console.log('db count is ' + count)
            for (var i = 0; i < count; i++) {
                if (typeof new_response[i]['pred'] !== 'undefined' && new_response[i]['pred'].length > 0){
                    for (var key in inference_result){
                        var amiid = new_response[i].amiid
                        if (parseInt(key.split('i')[1]) == amiid) {
                            inference_result[key]['pred_v'] = inference_result[key]['pred_v'].concat(new_response[i]['pred']);
                            inference_result[key]['true_v'] = inference_result[key]['true_v'].concat(new_response[i]['true']);
                            var time = new Date(new_response[i]['timestamp']).toISOString().replace(/T/, ' ').replace(/Z/, '');
                            for (var j = 0; j < new_response[i]['pred'].length; j++) {
                                inference_result[key]['loss'] = inference_result[key]['loss'].concat(response[i]['loss'])
                                inference_result[key]['average_loss'] = inference_result[key]['average_loss'].concat(response[i]['average_loss'])
                                inference_result[key]['time'].push(time);
                            }
                        }
                    }
                } else {
                    for (var key in inference_result){
                        inference_result[key]['pred_v'] = inference_result[key]['pred_v'].concat([-1]);
                        inference_result[key]['true_v'] = inference_result[key]['true_v'].concat([-1]);
                        inference_result[key]['time'].push(new Date(new_response[i]['updated_at_inferencedl']).toISOString().replace(/T/, ' ').replace(/Z/, ''));
                        inference_result[key]['loss'] = inference_result[key]['loss'].concat([-1]);
                        inference_result[key]['average_loss'] = inference_result[key]['average_loss'].concat([-1]);
                        updated_time.push(new Date(new_response[i]['updated_at_inferencedl']).toISOString().replace(/T/, ' ').replace(/Z/, ''));
                    }
                }
            }
            var new_max_value = 0;
            var new_max_value_loss = 0;
            var new_max_value_average_loss = 0;
            for (var key in inference_result){

                if (Math.max.apply(Math, inference_result[key]['true_v']) > new_max_value) {
                    new_max_value = Math.max.apply(Math, inference_result[key]['true_v']);
                }
                if (Math.max.apply(Math, inference_result[key]['pred_v']) > new_max_value) {
                    new_max_value = Math.max.apply(Math, inference_result[key]['pred_v']);
                }
                if (Math.max.apply(Math, inference_result[key]['loss']) > new_max_value_loss) {
                    new_max_value_loss = Math.max.apply(Math, inference_result[key]['loss']);
                }
                if (Math.max.apply(Math, inference_result[key]['average_loss']) > new_max_value_average_loss) {
                    new_max_value_average_loss = Math.max.apply(Math, inference_result[key]['average_loss']);
                }
            }
            if (max_value[1] < new_max_value){
              max_value[1] = new_max_value;
            }
            if (max_value[2] < new_max_value_loss){
              max_value[2] = new_max_value_loss;
            }
            if (max_value[3] < new_max_value_average_loss){
              max_value[3] = new_max_value_average_loss;
            }

            max_value[0] = response.length;

            console.log(inference_result);
            res.send({
                origin_count: origin_count,
                new_count: count,
                db_count: response.length,
                max_value: max_value,
                result: inference_result
            })
        })
    });

    app.get('/main/training/append_ami', function(req, res) {

        var model_name = req.query.model_name;
        var max_value = req.query.metadata;
        var origin_count = req.query.db;

        console.log(model_name);

        for(var i=0, item; item=models[i]; i++) {
            if (item['model_name']==model_name) {
                target_model = item;
                break
            }
        }

        var Training;
        console.log("111111. instanceTrain Info-------")
        console.log(instanceTrain);

        while (1) {
            if (target_model['model_name'] in instanceTrain.models) {
                instanceTrain.deleteModel(target_model['model_name'])
            } else {
                console.log("Mondb Connection State --- Not Connected")
                var Schema = instanceTrain.Schema;
                var trainingSchema = new mongoose.Schema({
                    amiid: Number,
                    pred: [Number],
                    true: [Number],
                    loss: [Number],
                    timestamp: Date,
                    update_at_onlinedl: Date
                }, {
                    collection: target_model['model_name']
                });
                Training = instanceTrain.model(target_model['model_name'], trainingSchema);
                console.log("Mondb Connection State --- Connected Success")
                break;
            }
        }

        console.log("222222. instanceTrain Info-------")
        console.log(Object.keys(instanceTrain.models));

        console.log(target_model);
        var training_result = {};
        for (var j = 0; j < target_model.amis.ami_id.length; j++) {
            var dict = {}
            dict['pred_v'] = []
            dict['true_v'] = []
            dict['loss'] = []
            dict['time'] = []
            training_result[target_model.amis.ami_id[j]] = dict;
        }

        Training.find(function(err, response){
            if(err) return res.status(500).send({error: 'database failure'});

            var count=0;
            var new_response = response.slice(origin_count);
            count = new_response.length
            console.log(training_result)
            console.log('db count is ' + count)
            for (var i = 0; i < count; i++) {
                if (typeof new_response[i]['pred'] !== 'undefined' && new_response[i]['pred'].length > 0){
                    for (var key in training_result){
                        var amiid = new_response[i].amiid
                        if (parseInt(key.split('i')[1]) == amiid) {
                            training_result[key]['pred_v'] = training_result[key]['pred_v'].concat(new_response[i]['pred'])
                            training_result[key]['true_v'] = training_result[key]['true_v'].concat(new_response[i]['true'])
                            var time = new Date(new_response[i]['timestamp']).toISOString().replace(/T/, ' ').replace(/Z/, '');
                            for (var j = 0; j < new_response[i]['pred'].length; j++) {
                                training_result[key]['loss'] = training_result[key]['loss'].concat(new_response[i]['loss'])
                                training_result[key]['time'].push(time);
                            }
                        }
                    }
                } else {
                    for (var key in training_result){
                        training_result[key]['pred_v'] = training_result[key]['pred_v'].concat([-1]);
                        training_result[key]['true_v'] = training_result[key]['true_v'].concat([-1]);
                        training_result[key]['loss'] = training_result[key]['loss'].concat([-1]);
                        training_result[key]['time'].push(new Date(new_response[i]['update_at_onlinedl']).toISOString().replace(/T/, ' ').replace(/Z/, ''));
                    }
                }
            }

            var new_max_value = 0;
            var new_max_value_loss = 0;
            for (var key in training_result){

                if (Math.max.apply(Math, training_result[key]['true_v']) > new_max_value) {
                    new_max_value = Math.max.apply(Math, training_result[key]['true_v']);
                }
                if (Math.max.apply(Math, training_result[key]['pred_v']) > new_max_value) {
                    new_max_value = Math.max.apply(Math, training_result[key]['pred_v']);
                }
                if (Math.max.apply(Math, training_result[key]['loss']) > new_max_value_loss) {
                    new_max_value_loss = Math.max.apply(Math, training_result[key]['loss']);
                }
            }
            if (max_value[1] < new_max_value){
              max_value[1] = new_max_value;
            }
            if (max_value[2] < new_max_value_loss){
              max_value[2] = new_max_value_loss;
            }
            max_value[0] = response.length;

            console.log(training_result);

            res.send({
                origin_count: origin_count,
                new_count: count,
                db_count: response.length,
                max_value: max_value,
                result: training_result
            })
        })
    });

    app.get('/main/deploy_model_info', function(req, res){
        console.log(select_model);
        if (select_model == "none") {
            console.log("go to model_management page")
            res.render('model_management', {
                title: "model_management",
                models: models
            })
        } else {
            target_model = select_model;
            console.log(target_model['amis']);
            var txt = "";
            for (var j = 0; j < target_model['amis']['ami_id'].length; j++) {
                txt = txt + target_model['amis']['ami_id'][j] + " ";
            }

            target_model['ami'] = txt

            res.render('deploy_model_info', {
                title: "deploy_model_info",
                model: target_model
            })
        }
    });

    app.get('/main/inference', function(req, res){
        if (select_model == "none") {
            res.render('model_management', {
                title: "model_management",
                models: models
            })
        } else {

        }
    });

    app.get('/main/training', function(req, res){
        if (select_model == "none") {
            res.render('model_management', {
                title: "model_management",
                models: models
            })
        } else {

        }
    });

    function guid() {
        function s4() {
            return ((1 + Math.random()) * 0x10000 | 0).toString(16).substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
    }
}
