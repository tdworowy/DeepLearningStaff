import * as React from 'react';
import { networkDetailsEndPoint,dataSetsEndPoint,compileNetwrokEndPoint,trainNetwrokEndPoint,plotAccEndPoint,plotLossEndPoint } from './Config';
import { SyncRequestClient } from 'ts-sync-request/dist'
import { Url } from 'url';

class CompileNetworkData {
    name: string|File|null
    optimizer: string|File|null
    loss: string|File|null
    metrics: Array<String|File|null>

    constructor(name:string|File|null,optimizer:string|File|null,loss:string|File|null,metrics:Array<string|File|null>) {
        this.name = name
        this.optimizer = optimizer
        this.loss = loss
        this.metrics = metrics
    }

}

const sleep = (milliseconds:number) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))}

function getNetworkDetailsSync(networkName:string | undefined) {
     return new SyncRequestClient()
            .addHeader("Content-Type", "application/json")
            .get<Response>(networkDetailsEndPoint + networkName)
   
}
function getDataSetsSync() {
    return new SyncRequestClient()
        .addHeader("Content-Type", "application/json")
        .get<Response>(dataSetsEndPoint)
}

function compileNetworkSync(data:any) {
    return new SyncRequestClient()
    .addHeader("Content-Type", "application/json")
    .post<Url,any>(compileNetwrokEndPoint,data)
}
function trainNetworkSync(data:any) {
    return new SyncRequestClient()
    .addHeader("Content-Type", "application/json")
    .post<Url,any>(trainNetwrokEndPoint,data)
}


export interface ViewProperties {
    params: string
}
interface InetworkDetails {
    Name:string
    Compiled: boolean
    Trained: boolean
}
type State = { name:string, form:any };
export class NetworkDetails extends React.Component<ViewProperties,State> {

    constructor(props:ViewProperties) {
        super(props);
        this.state = {name: this.props.params, form: undefined} 
    }

    compileNetworkHandler = (event:any) => {
        const data = new FormData(event.target)
        const compileNetworkData = new CompileNetworkData(
            data.get("name"),
            data.get("optimizer"),
            data.get("loss"),
            [data.get("metrics")]
        )
        const json = JSON.stringify(compileNetworkData)
        console.log(`POST:${json}`) 
        compileNetworkSync(compileNetworkData)
     
    }
    trainNetworkHandler = (event:any) => {
        const data = new FormData(event.target)
        const json = JSON.stringify(Object.fromEntries(data))
        console.log(`POST:${json}`)
        trainNetworkSync(Object.fromEntries(data))
    }
    getDataSources() {
        var dat_sources: Array<string> = []
        var data:any = getDataSetsSync()
        if(data.Dat_Sources !== "") {
               console.log(`Response:${JSON.stringify(data)}`)
               dat_sources = data.Dat_Sources
            }
       return dat_sources
    }    
    createDataSources = () => {
        let data_sources:Array<JSX.Element> = []
        if ( this.getDataSources().length > 0) {
            this.getDataSources().forEach(function (value) {
                console.log(value) 
                data_sources.push(
                            <option value={value}>
                             {value}
                            </option>)
            })
        }
        return data_sources
      }
 
    compileForm() {
        return (
        <div className="container">    
        <form onSubmit={this.compileNetworkHandler}>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="name">Network name:</label>
        </div>
        <div className="col-75">    
                        <input
                        readOnly
                        name = 'name'
                        type = 'text'
                        defaultValue = {this.state.name}
                        />
        </div>
        </div>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="optimizer">Optimizer:</label>
        </div>
        <div className="col-75">  
                        <select
                        name = 'optimizer'
                        >
                        <option value='sgd'>SGD</option>
                        <option value='rmsprop'>rmsprop</option>     
                        <option value='adagrad'>Adagrad</option>      
                        <option value='adadelta'>Adadelta</option>
                        <option value='adam'>Adam</option>
                        <option value='adamax'>Adamax</option> 
                        <option value='nadam'>Nadam</option>     
                        </select>
        </div>
        </div>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="loss">Loss:</label>
        </div>
        <div className="col-75">  
                        <select
                        name = 'loss'
                        >
                        <option value='mean_squared_error'>mean_squared_error</option>
                        <option value='mean_absolute_error'>mean_absolute_error</option>
                        <option value='mean_absolute_percentage_error'>mean_absolute_percentage_error</option>
                        <option value='mean_squared_logarithmic_error'>mean_squared_logarithmic_error</option>
                        <option value='squared_hinge'>squared_hinge</option>
                        <option value='hinge'>hinge</option>
                        <option value='categorical_hinge'>categorical_hinge</option>
                        <option value='logcosh'>logcosh</option>
                        <option value='huber_loss'>huber_loss</option>
                        <option value='categorical_crossentropy'>categorical_crossentropy</option>
                        <option value='sparse_categorical_crossentropy'>sparse_categorical_crossentropy</option>
                        <option value='binary_crossentropy'>binary_crossentropy</option>
                        <option value='kullback_leibler_divergence'>kullback_leibler_divergence</option>
                        <option value='poisson'>poisson</option>
                        <option value='cosine_proximity'>cosine_proximity</option>
                        <option value='is_categorical_crossentropy'>is_categorical_crossentropy</option>
                        <option value='is_categorical_crossentropy'>is_categorical_crossentropy</option>
                        </select>
        </div>
        </div>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="metrics">Metrics:</label>
        </div>
        <div className="col-75">        
                        <select
                        name = 'metrics'
                        >
                        <option value='acc'>accuracy</option>    
                        <option value='binary_accuracy'>binary_accuracy</option>
                        <option value='categorical_accuracy'>categorical_accuracy</option>   
                        <option value='sparse_categorical_accuracy'>sparse_categorical_accuracy</option>
                        <option value='top_k_categorical_accuracy'>top_k_categorical_accuracy</option>
                        <option value='sparse_top_k_categorical_accuracy'>sparse_top_k_categorical_accuracy</option>
                        <option value='cosine_proximity'>cosine_proximity</option>                                
                        </select> 
        </div>
        </div>
                    <input id="compile" type="submit" value="Compile network"/>
        </form>
        </div>
        )
    }
    
    trainForm() {
        return (
        <div className="container">    
        <form onSubmit={this.trainNetworkHandler}>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="name">Network name:</label>
        </div>
        <div className="col-75">   
                        <input
                        readOnly
                        name = 'name'
                        type = 'text'
                        defaultValue = {this.state.name}
                        />
        </div>
        </div>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="data_set">Data set:</label>
        </div>
        <div className="col-75"> 
                        <select
                        name = 'data_set'
                        >
                       {this.createDataSources()} 
                    </select>    
        </div>
        </div>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="epochs">Epochs:</label>
        </div>
        <div className="col-75"> 
                        <input
                        name = 'epochs'
                        type ='number'
                        />
        </div>
        </div>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="batch_size">Batch size:</label>
        </div>
        <div className="col-75"> 
                        <input
                        name = 'batch_size'
                        type ='number'
                        />
        </div>
        </div>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="input_shape">Input shape:</label>
        </div>
        <div className="col-75"> 
                        <input
                        name = 'input_shape'
                        type ='number'
                        />
        </div>
        </div>
        <div className="row">
        <div className="col-25">
        <label htmlFor ="test_sample_size">Test sample size:</label>
        </div>
        <div className="col-75"> 
       
                        <input
                        name = 'test_sample_size'
                        type ='text'
                        />
        </div>
        </div>
                    <input id="train" type="submit" value="Train network"/>
        </form>
        </div>
        )
    }

    getNetworkDetails() {
       return getNetworkDetailsSync(this.state.name)
    }
    getPlotAcc() {
        return plotAccEndPoint + this.state.name
    } 
    getPlotLoss() {
        return plotLossEndPoint + this.state.name
    }  
   
    getForm():any {
        var details:any = this.getNetworkDetails()
        console.log(`Network details in getFrom:${JSON.stringify(details)}`)
        if (details.Compiled === false) {
             return this.compileForm()
        }
        if (details.Trained === false) {
           return this.trainForm()
        }
        else {
            return (
                <div>
                     <iframe id="acc_frame" src= {this.getPlotAcc()}  /> 
                     <iframe id="loss_frame" src= {this.getPlotLoss()} />
                </div>
                
            ) 
        }

    }
    render() {
        return (
            <div>
                {this.getForm()}
                <br/>
                <textarea id="network_details" rows={50} cols={50} value={JSON.stringify(this.getNetworkDetails())}></textarea>
            </div>
        )}
}
