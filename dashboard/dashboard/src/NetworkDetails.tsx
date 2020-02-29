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
function getPlotAccSync(name:string) {
    return new SyncRequestClient()
        .addHeader("Content-Type", "application/json")
        .get<Response>(plotAccEndPoint+name)
}
function getPlotLossSync(name:string) {
    return new SyncRequestClient()
        .addHeader("Content-Type", "application/json")
        .get<Response>(plotLossEndPoint+name)
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
async function compileNetwork(data:any) {
    const response = await fetch(compileNetwrokEndPoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: data
        })
    return await response.json()
}
async function trainNetwork(data:any) {
    const response = await fetch(trainNetwrokEndPoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: data
        })
    return await response.json()
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
        <form onSubmit={this.compileNetworkHandler}>
                    Network name:&nbsp;&nbsp;
                        <input
                        readOnly
                        name = 'name'
                        type = 'text'
                        defaultValue = {this.state.name}
                        />
                    <br/>
                    optimizer:&nbsp;&nbsp;
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
                    <br/>
                    loss:&nbsp;&nbsp;
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
                    <br/>
                    
                    metrics:&nbsp;&nbsp;
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
                    <br/>
                    <input id="compile" type="submit" value="Compile network"/>
        </form>
        )
    }
    
    trainForm() {
        return (
        <form onSubmit={this.trainNetworkHandler}>
                    Network name:&nbsp;&nbsp;
                        <input
                        readOnly
                        name = 'name'
                        type = 'text'
                        defaultValue = {this.state.name}
                        />
                    <br/>
                    data_set:&nbsp;&nbsp;
                        <select
                        name = 'data_set'
                        >
                       {this.createDataSources()} 
                    </select>    
                    <br/>
                    epochs:&nbsp;&nbsp;
                        <input
                        name = 'epochs'
                        type ='number'
                        />
                    <br/>
                    batch_size:&nbsp;&nbsp;
                        <input
                        name = 'batch_size'
                        type ='number'
                        />
                    <br/>
                    input_shape:&nbsp;&nbsp;
                        <input
                        name = 'input_shape'
                        type ='number'
                        />
                    <br/>
                    test_sample_size:&nbsp;&nbsp;
                        <input
                        name = 'test_sample_size'
                        type ='text'
                        />
                    <br/>
                    <input id="train" type="submit" value="Train network"/>
        </form>
        )
    }

    getNetworkDetails() {
       return getNetworkDetailsSync(this.state.name)
    }
    getPlotAcc() {
        return getPlotAccSync(this.state.name)
     } 
     getPlotLoos() {
        return getPlotLoosSync(this.state.name)
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
                {this.getPlotAcc()}
                {this.getPlotLoos()}
                </div>
            )
        }

    }
    render() {
        return (
            <div>
                {this.getForm()}
                <textarea id="network_details" rows={4} cols={50} value={JSON.stringify(this.getNetworkDetails())}></textarea>
            </div>
        )}
}
