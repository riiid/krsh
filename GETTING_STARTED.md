# Getting Startted

### Step01 - Create Project

First of all, you need to create a KRSH project. To create a KRSH Project, you can create it with the command below. 
```bash
krsh create project $PROJECT_NAME
cd $PROJECT_NAME

# outputs directory
# $PROJECT_NAME/
# - components/
# - dockerfiles/
# - pipelines/
```

### Step02 - Configure

After you navigate to the krsh project you created, perform the basic configure using the command below.
This command allows you to set up kubeflow `host` and `namespace`. The kubeflow `host` must be configured in the same format as `https://{DOMAIN}/pipeline`.
```bash
krsh configure
```

### Step03 - Create Pipeline
You can create a Pipeline Template using the command below. The generated pipeline is located in `pipelines/$PIPELINE_NAME`.

```bash
krsh create pipeline $PIPELINE_NAME

# outputs directory
# $PIPELINE_NAME output
# - pipeline.yaml
# - pipeline.py  <- Modify this file to create a pipeline!
```

### Step04 - Plan

Check in action what happens when you apply.
```bash
krsh plan
```

### Step05 - Apply

Apply the defined pipeline spec to Kubeflow.
```bash
krsh apply
```

### Optional - Create Component

If you want to create reusable components, create them with the command below. The component is created in `components/$COMPONENT_NAME/`.
```bash
krsh create component $COMPONENT_NAME
```

### Optional - Deploy to Multi Namespace

If you want to deploy a pipeline to multiple Namespaces, enter multiple namespaces in `pipeline.yaml`. And the namespace list here must all be entered in `configuration.yaml`.

```yaml
# pipeline.yaml
entry_point: pipeline.py
name: hello-pipeline
namespaces:
- namespace-1
- namespace-2
- namespace-3

```