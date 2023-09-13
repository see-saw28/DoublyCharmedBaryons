'''
import ROOT
def merge_root_output(j, input_tree_name, merged_filepath):
    # Treat a job with subjobs the same as a job with no subjobs
    sjobs = j.subjobs
    if len(sjobs) == 0:
        sjobs = [j]

    access_urls = []
    for sj in sjobs:
        if sj.status != 'completed':
            print ('Skipping #{0}'.format(sj.id))
            continue
        for df in sj.outputfiles.get(DiracFile):
            access_urls.append(df.accessURL())

    tchain = ROOT.TChain(input_tree_name)
    for url in access_urls:
        tchain.Add(url)
    tchain.Merge(merged_filepath)
'''
import os
import subprocess
import numpy as np

def merge_root_output(j, merged_filepath,fileDescription, nbSubjobs = -1):
    import os
    # Treat a job with subjobs the same as a job with no subjobs
    # if no subjobs why would I be merging root output???
    try:
        sjobs = j.subjobs
        if len(sjobs) == 0:
            sjobs = [j]
    except AttributeError:
        #if already broken down into subjobs
        #doesnt try and extract subjobs
        sjobs = j

    access_urls = []

    if nbSubjobs != -1:
        sjobs = sjobs[0:nbSubjobs]
    for sj in sjobs:
        if sj.status != 'completed':
            print('Skipping #{0}'.format(sj.id))
            continue
        for df in sj.outputfiles.get(DiracFile):
            if (df.accessURL()!=[]):
                access_urls.append(df.accessURL()[0])

    all_urls=" ".join(map(str,access_urls))
    print(all_urls)
    subprocess.run("lb-conda default hadd -fk "+merged_filepath+"/job%i-CombDVntuple-%s.root "%(sjobs[-1].master.id,fileDescription)+all_urls, shell=True)

def merge_root_output_split(JOBS, merged_filepath,fileDescription='', nbSubjobs = 150,startJob=0,endJob=0):
    import os
    # Treat a job with subjobs the same as a job with no subjobs
    # if no subjobs why would I be merging root output???
    # try:
    #     sjobs = j.subjobs
    #     if len(sjobs) == 0:
    #         sjobs = [j]
    # except AttributeError:
    #     #if already broken down into subjobs
    #     #doesnt try and extract subjobs
    #     sjobs = j

    if type(JOBS) == int :
        JOBS = [JOBS]

    if (startJob!=0) & (endJob!=0) :
        JOBS = list(range(startJob, endJob+1))

    for k,jobID in enumerate(JOBS) :
        sjobs = jobs(jobID).subjobs
        print(f"Downloading job {jobID}")
        access_urls = []

        for sj in sjobs:
            if sj.status != 'completed':
                print('Skipping #{0}'.format(sj.id))
                continue
            for df in sj.outputfiles.get(DiracFile):
                if (df.accessURL()!=[]):
                    access_urls.append(df.accessURL()[0])
                else :
                    print('No output file #{0}'.format(sj.id))

        access_urls_cut = access_urls
        print( access_urls)
        # access_urls_cut = []
        # for url in access_urls:
        #     if 'infn' not in url:
        #         access_urls_cut.append(url)
        # print(len(access_urls),'urls but only',len(access_urls_cut),'available')
        nbURLs = len(access_urls_cut)
        if type(nbSubjobs)==int:
            sjSplit = nbSubjobs
        elif type(nbSubjobs)==list:
            sjSplit = nbSubjobs[k]

        split = int(np.ceil(nbURLs/sjSplit))
        for i in range(0,split):
            all_urls=" ".join(map(str,access_urls_cut[i*sjSplit:(i+1)*sjSplit]))
            print(f'Merging n°{i}')
            # filename = sj.outputfiles[0].lfn.split('/')[-1].split('.')[0].replace("_","-")
            filename = jobs(jobID).name
            subprocess.run("lb-conda default hadd -fk "+merged_filepath+"/job%i-%s%s-%i.root "%(sjobs[-1].master.id,filename,fileDescription,i)+all_urls, shell=True)


def resubmit_failed_jobs(j):
    try:
        sjobs = j.subjobs
        if len(sjobs) == 0:
            sjobs = [j]
    except AttributeError:
        #if already broken down into subjobs
        #doesnt try and extract subjobs
        sjobs = j

    failed = False    
    for sj in sjobs:
        if (sj.status == 'failed'):
            print(f'Job {sj.id} resubmited')
            sj.resubmit()
            failed = True

    if not failed :
        print('No job have failed')

def resubmit_completing_jobs(j):
    try:
        sjobs = j.subjobs
        if len(sjobs) == 0:
            sjobs = [j]
    except AttributeError:
        #if already broken down into subjobs
        #doesnt try and extract subjobs
        sjobs = j

    reset = False    
    for sj in sjobs:
        if (sj.status == 'completing'):
            print(f'Job {sj.id} backend reset')
            sj.backend.reset()
            reset = True

    if not reset :
        print('No job completing')


def download_output(JOBS):
    if type(JOBS) == int :
        JOBS = [JOBS]
    
    for jobID in JOBS :
        job = jobs(jobID)
        for i in range(0,len(job.subjobs)):
            k = job.id
            if job.subjobs[i].status=='completed':
                file = 'echo Copying %d %d/%d' % (k, i, len(job.subjobs))
                os.system(file)
                os.system('mkdir -p /tmp/pgaigne/%d/%d/output' % (k, i))
                dir = '/tmp/pgaigne/%d/%d/output' % (k, i)
                job.subjobs[i].backend.getOutputData(dir)
            else:
                print(f'Skipping {k} {i}')

def merge_local_output_split(jobID, merged_filepath, nbSubjobs):
    fileslist = []
    for root, dirs, files in os.walk(f"/tmp/pgaigne/{jobID}", topdown=False):
        for name in files:
            fileslist.append(os.path.join(root, name))

    split = int(np.ceil(len(fileslist)/nbSubjobs))
    for i in range(0,split):
        all_urls=" ".join(map(str,fileslist[i*nbSubjobs:(i+1)*nbSubjobs]))
        print(f'Merging n°{i}')
        subprocess.run("lb-conda default hadd -fk "+merged_filepath+"/job%i-CombDVntuple-%s-%i.root "%(jobID,jobs(jobID).name,i)+all_urls, shell=True)

def merge_local_output(JOBS, merged_filepath):
    if type(JOBS) == int :
        JOBS = [JOBS]
    
    for jobID in JOBS :
        print(f'Merging {jobID}')
        fileslist = []
        for root, dirs, files in os.walk(f"/tmp/pgaigne/{jobID}", topdown=False):
            for name in files:
                fileslist.append(os.path.join(root, name))

        all_urls=" ".join(map(str,fileslist))
        subprocess.run("lb-conda default hadd -fk "+merged_filepath+"/job%i-CombDVntuple-%s.root "%(jobID,jobs(jobID).name)+all_urls, shell=True)

    

def delete_jobs(JOBS=0,startJob=0,endJob=0):
    if JOBS!=0:
        if type(JOBS) == int :
            Jobs = [JOBS]
        else :
            Jobs =JOBS
    
    if (startJob!=0) & (endJob!=0) :
        Jobs = list(range(startJob, endJob+1))
    print(Jobs)
    for jobID in Jobs :
        sj = jobs(jobID)

        if (sj.status == 'failed'):
            sj.remove()
            print(f'Job {sj.id} deleted')
        else :
            sj.force_status("failed",force=True)
            sj.remove()
            print(f'Job {sj.id} deleted')

            