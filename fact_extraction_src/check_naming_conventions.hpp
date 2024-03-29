#ifndef CHECKNAMINGCONVENTIONSPOLICY
#define CHECKNAMINGCONVENTIONSPOLICY

#include <ClassPolicy.hpp>
#include <srcSAXHandler.hpp>
#include <DeclTypePolicy.hpp>
#include <ParamTypePolicy.hpp>
#include <srcSAXEventDispatcher.hpp>
#include <FunctionSignaturePolicy.hpp>

struct IdentifierData{
    IdentifierData(std::string type, std::string name, std::string context, std::string fileName, std::string programmingLanguageName, std::string lineNumber, bool isPointer, bool isArray) 
    : type{type}, name{name}, context{context}, fileName{fileName}, programmingLanguageName{programmingLanguageName}, lineNumber{lineNumber}, isPointer(isPointer), isArray(isArray) {}
    
    std::string type;
    std::string name;
    std::string context;
    std::string lineNumber;
    std::string fileName;
    std::string programmingLanguageName;
    bool isPointer;
    bool isArray;

    friend std::ostream& operator<<(std::ostream& outputStream, const IdentifierData& identifier){
        outputStream<<identifier.type<<","<<identifier.name<<","<<identifier.context<<","
                    <<identifier.lineNumber<<","<<identifier.fileName<<","<<identifier.programmingLanguageName<<","
                    <<identifier.isPointer<<","<<identifier.isArray;
        return outputStream;
    }
};

class CheckNamingConventionsPolicy : public srcSAXEventDispatch::EventListener, public srcSAXEventDispatch::PolicyDispatcher, public srcSAXEventDispatch::PolicyListener 
{
    public:
        CheckNamingConventionsPolicy(std::initializer_list<srcSAXEventDispatch::PolicyListener*> listeners = {}) : srcSAXEventDispatch::PolicyDispatcher(listeners) {
            
            InitializeEventHandlers();
            declPolicy.AddListener(this);
            paramPolicy.AddListener(this);
            functionPolicy.AddListener(this);
        }
        void Notify(const PolicyDispatcher *policy, const srcSAXEventDispatch::srcSAXEventContext &ctx) override {
            using namespace srcSAXEventDispatch;
            if(typeid(DeclTypePolicy) == typeid(*policy)){
                declarationData = *policy->Data<DeclData>();
                if(!(declarationData.nameOfIdentifier.empty()||declarationData.nameOfType.empty())){
                    if(ctx.IsOpen(ParserState::function)){
                        if(declarationData.isPointer) declarationData.nameOfType += "*";
                        if(declarationData.usesSubscript) declarationData.nameOfType += "[]";
                        CollectIdentifierTypeNameAndContext(declarationData.nameOfType, declarationData.nameOfIdentifier, "DECLARATION", ctx.currentLineNumber, 
                                                            ctx.currentFilePath, ctx.currentFileLanguage, declarationData.isPointer, declarationData.usesSubscript);

                    }else if(ctx.IsOpen(ParserState::classn) && !declarationData.nameOfContainingClass.empty() && !declarationData.nameOfType.empty() 
                             && !declarationData.nameOfIdentifier.empty()){
                        
                        CollectIdentifierTypeNameAndContext(declarationData.nameOfType, declarationData.nameOfIdentifier, "ATTRIBUTE", ctx.currentLineNumber, 
                                                            ctx.currentFilePath, ctx.currentFileLanguage, declarationData.isPointer, declarationData.usesSubscript);

                    }
                }
            }else if(typeid(ParamTypePolicy) == typeid(*policy)){
                parameterData = *policy->Data<DeclData>();
                if(!(parameterData.nameOfIdentifier.empty() || parameterData.nameOfType.empty())){
                    if(parameterData.isPointer) parameterData.nameOfType += "*";
                    if(parameterData.usesSubscript) parameterData.nameOfType += "[]";
                    CollectIdentifierTypeNameAndContext(parameterData.nameOfType, parameterData.nameOfIdentifier, "PARAMETER", ctx.currentLineNumber, 
                                                        ctx.currentFilePath, ctx.currentFileLanguage, parameterData.isPointer, parameterData.usesSubscript);

                }
            }else if(typeid(FunctionSignaturePolicy) == typeid(*policy)){
                functionData = *policy->Data<SignatureData>();
                if(!(functionData.name.empty() || functionData.returnType.empty())){
                    CollectIdentifierTypeNameAndContext(functionData.returnType, functionData.name, "FUNCTION", ctx.currentLineNumber, 
                                                        ctx.currentFilePath, ctx.currentFileLanguage, 0, 0);
                }
            }
        }
        
        void NotifyWrite(const PolicyDispatcher *policy, srcSAXEventDispatch::srcSAXEventContext &ctx){}

        void CollectIdentifierTypeNameAndContext(std::string identifierType, std::string identifierName, std::string codeContext,
                                                 unsigned int lineNumber, std::string fileName, std::string programmingLanguageName, 
                                                 bool isPointer, bool isArray){
                allSystemIdentifiers.push_back(IdentifierData(identifierType, identifierName, codeContext, std::to_string(lineNumber), fileName, programmingLanguageName, isPointer, isArray));
        }        
        
    protected:
        void *DataInner() const override {
            return (void*)0; // export profile to listeners
        }
        
    private:
        std::vector<IdentifierData> allSystemIdentifiers;
        DeclTypePolicy declPolicy;
        DeclData declarationData;

        ParamTypePolicy paramPolicy;
        DeclData parameterData;

        FunctionSignaturePolicy functionPolicy;
        SignatureData functionData;

        void InitializeEventHandlers(){
            using namespace srcSAXEventDispatch;
            
            //Open events
            openEventMap[ParserState::declstmt] = [this](srcSAXEventContext& ctx){
                ctx.dispatcher->AddListenerDispatch(&declPolicy);
            };
            openEventMap[ParserState::parameterlist] = [this](srcSAXEventContext& ctx) {
                ctx.dispatcher->AddListenerDispatch(&paramPolicy);
            };
            openEventMap[ParserState::function] = [this](srcSAXEventContext& ctx) {
                ctx.dispatcher->AddListenerDispatch(&functionPolicy);
            };

            //Close events
            closeEventMap[ParserState::classn] = [this](srcSAXEventContext& ctx){
                if(!ctx.currentClassName.empty()){

                    CollectIdentifierTypeNameAndContext("class", ctx.currentClassName, "CLASS", ctx.currentLineNumber, 
                                                        ctx.currentFilePath, ctx.currentFileLanguage, 0, 0);
                }
            };
            closeEventMap[ParserState::functionblock] = [this](srcSAXEventContext& ctx){
                ctx.dispatcher->RemoveListenerDispatch(&functionPolicy);
            };
            closeEventMap[ParserState::declstmt] = [this](srcSAXEventContext& ctx){
                ctx.dispatcher->RemoveListenerDispatch(&declPolicy);
            };
            closeEventMap[ParserState::parameterlist] = [this](srcSAXEventContext& ctx) {
                ctx.dispatcher->RemoveListenerDispatch(&paramPolicy);
            };
            closeEventMap[ParserState::archive] = [this](srcSAXEventContext& ctx) {
                std::cout<<"type,"<<"name,"<<"context,"<<"language,"<<"line,"<<"filename,"<<"pointer,"<<"array,"<<std::endl;
                for(auto identifier : allSystemIdentifiers){
                    std::cout<<identifier<<std::endl;
                }
            };
        }
};
#endif