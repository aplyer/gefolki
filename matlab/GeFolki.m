%     « Copyright (c) 2016, Elise Koeniguer, Aurélien Plyer (Onera) » 
%     This file is part of GeFolki.
% 
%     GeFolki is free software: you can redistribute it and/or modify
%     it under the terms of the GNU General Public License as published by
%     the Free Software Foundation, either version 3 of the License, or
%     (at your option) any later version.
% 
%     GeFolki is distributed in the hope that it will be useful,
%     but WITHOUT ANY WARRANTY; without even the implied warranty of
%     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%     GNU General Public License for more details.
% 
%     You should have received a copy of the GNU General Public License
%     along with GeFolki in the file copying.txt.  
%     If not, see <http://www.gnu.org/licenses/gpl.txt>.
%
% ------------------------------------------------------------------------
%
%     GeFolki est un logiciel libre ; vous pouvez le redistribuer ou le
%     modifier suivant les termes de la GNU General Public License telle
%     que publiée par la Free Software Foundation ; soit la version 3 de la
%     licence, soit (à votre gré) toute version ultérieure.
% 
%     GeFolki est distribué dans l'espoir qu'il sera utile, mais SANS
%     AUCUNE GARANTIE ; sans même la garantie tacite de QUALITÉ MARCHANDE
%     ou d'ADÉQUATION à UN BUT PARTICULIER. Consultez la GNU General Public
%     License pour plus de détails.
% 
%     Vous devez avoir reçu une copie de la GNU General Public License en
%     même temps que Gefolki dans le fichier copying.txt ; si ce n'est pas
%     le cas, consultez % <http://www.gnu.org/licenses/gpl.txt


function w = GeFolki(I0, I1, para)



if ~exist('para','var')
    para = struct('radius' , 32:-4:8, ...
        'levels' , 6, ...
        'iter' , 2, ...
        'contrast_adapt', false, ...
        'rank', 4);
end

I0 = single(I0);
I1 = single(I1);




if para.contrast_adapt % For decision about contrast inversion
    I0 = (I0-min(I0(:))) ./ (max(I0(:))-min(I0(:)));
    I1 = (I1-min(I1(:))) ./ (max(I1(:))-min(I1(:)));
end


% Pyramidal decomposition of each image of the pair
pyrI0 = pyramid(I0, para.levels);
pyrI1 = pyramid(I1, para.levels);


for n = size(pyrI0,1):-1:1
    
    
    J0 = pyrI0{n};
    J1 = pyrI1{n};
    if para.contrast_adapt
        H0 = adapthisteq(J0);
        H1 = adapthisteq(J1);
    else
        H0 = J0;
        H1 = J1;
    end
    
    [row, col] = size(J0);
    [x, y] = meshgrid(1:col, 1:row);
    
    if(n ~= size(pyrI0,1))
        u = expand(u,size(J0));
        v = expand(v,size(J0));
        
        
    else
        u = zeros(size(J0));
        v = zeros(size(J0));
    end
    
    if para.rank ~= 0
        I0 = rank_filter(J0,para.rank);
        I1_sup = rank_filter(J1,para.rank);
        I1_inf = rank_filter(J1, -para.rank);
    else
        I0 = J0;
        I1_sup = J1;
        I1_inf = 1-I1;
    end
    
    
    [Ix, Iy] = gradient(I0);
    Ixx = (Ix.*Ix);
    Iyy = (Iy.*Iy);
    Ixy = (Ix.*Iy);
    
    
    
    
    for r = para.radius
        fen = ones(1,2*r+1);
        
        
        A = convSep(Ixx,fen);
        B = convSep(Iyy,fen);
        C = convSep(Ixy,fen);
        
        for i = 1:para.iter
            dx = x + u;
            dy = y + v;
            dx(dx < 1) = 1;
            dy(dy < 1) = 1;
            dx(dx > col) = col;
            dy(dy > row) = row;
            
            
            I1w_sup = interp2gpu(I1_sup,dx,dy);
            I1w = I1w_sup;
            
            if para.contrast_adapt == true
                H1w = interp2gpu(H1,dx,dy);
                wi = ones(1,para.rank*2+1);

                crit1 = convSep(abs(H0-H1w),wi);
                crit2 = convSep(abs(1-H0-H1w), wi);
                I1w_inf = interp2gpu(I1_inf,dx,dy);
                I1w(crit1 > crit2) = I1w_inf(crit1 > crit2);
                
            end
            

            
            
            
            %% FOLKI resolution
            It = I0 - I1w + u.*Ix + v.*Iy;
            G=It.*Ix;
            H=It.*Iy;
            
            G = convSep(G,fen);
            H = convSep(H,fen);
            D = A.*B - C.*C;
            u = (G.*B - C.*H) ./ D;
            v = (A.*H - C.*G) ./ D;
            u(isnan(u)) = 0;
            v(isnan(v)) = 0;
            
            
            
        end
    end
end


w=cat(3,u,v);


function P = pyramid(I,lvl)
P=cell(lvl+1,1);
P{1}=I;
for k=1:lvl,
    P{k+1}=(pyramBurt(P{k}));
end
        
       
function N = pyramBurt(M)
a = 0.4;
burt1D = [1/4-a/2,1/4,a,1/4,1/4-a/2];
N = convSep(M,burt1D);
N = N(1:2:end,1:2:end);
            
                
function ue = expand(u,s)
ue = imresize(u,s)./0.5;


function res = convSep(I,fen)
res = conv2(conv2(I,fen','same'),fen,'same');


function Iw = interp2gpu(I,x,y)
x = floor(x*256)/256;
y = floor(y*256)/256;
Iw = interp2(I,x,y,'linear');
                            

