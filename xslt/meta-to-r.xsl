<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exsl="http://exslt.org/common"
 xmlns:str="http://exslt.org/strings"
 extension-element-prefixes="exsl str"
 xmlns:data="any-uri">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

 <data:map-order>
  <locusname order="1">D6S2239</locusname>
  <locusname order="2">D6S2223</locusname>
  <locusname order="3">D6S2222</locusname>
  <locusname order="4">A</locusname>
  <locusname order="5">D6S265</locusname>
  <locusname order="6">C</locusname>
  <locusname order="7">B</locusname>
  <locusname order="8">MIB</locusname>
  <locusname order="9">TNFD</locusname>
  <locusname order="10">D6S273</locusname>
  <locusname order="11">DRA</locusname>
  <locusname order="12">DRB1</locusname>
  <locusname order="13">DQA1</locusname>
  <locusname order="14">DQIV</locusname>
  <locusname order="15">DQCARII</locusname>
  <locusname order="16">DQCAR</locusname>
  <locusname order="17">DQB1</locusname>
  <locusname order="18">G51152</locusname>
  <locusname order="19">DPA1</locusname>
  <locusname order="20">DPB1</locusname>
  <locusname order="21">D6S291</locusname>
 </data:map-order>

 <data:region-order>
  <regionname long="Sub-Saharan-Africa">01.SS-Africa</regionname>
  <regionname long="North-Africa">02.N-Africa</regionname>	  
  <regionname long="Europe">03.Europe</regionname>	  
  <regionname long="South-West-Asia">04.SW-Asia</regionname>	  
  <regionname long="South-East-Asia">05.SE-Asia</regionname>	  
  <regionname long="Oceania">06.Oceania</regionname>	  
  <regionname long="Australia">07.Australia</regionname>	  
  <regionname long="North-East-Asia">08.NE-Asia</regionname>	  
  <regionname long="North-America">09.N-America</regionname>	  
  <regionname long="South-America">10.S-America</regionname>	  
  <regionname long="Other">11.Other</regionname>          
 </data:region-order>

 <xsl:param name="map-order" 
  select="document('')//data:map-order/locusname"/>

 <xsl:param name="region-order" 
  select="document('')//data:region-order/regionname"/>

 <xsl:variable name="all-allele-list" select="document('allelelist-by-locus.xml', .)/allelelist-by-locus"/>

 <xsl:param name="header-line-start">pop&#09;ethnic&#09;region&#09;latit&#09;longit&#09;complex&#09;</xsl:param>

 <xsl:template name="output-field">
  <xsl:param name="node"/>

  <xsl:choose>
   <xsl:when test="$node!=''">
    <xsl:value-of select="$node"/>
   </xsl:when>
   <xsl:otherwise>****</xsl:otherwise>
  </xsl:choose>

  <!-- output tab -->
  <xsl:text>&#09;</xsl:text>
  
 </xsl:template>


 <!-- suppress output of random text -->
 <xsl:template match="text()"/>

 <xsl:template name="phylip-lines">
  <xsl:param name="nodes"/>

  <xsl:text>     </xsl:text>
  <xsl:value-of select="count($nodes)"/>
  <xsl:text> </xsl:text>
  <xsl:value-of select="count($all-allele-list/locus[.!=''])"/>
  <xsl:call-template name="newline"/>

  <xsl:for-each select="$all-allele-list/locus">
   <xsl:if test="count(allele)!=0">
    <xsl:value-of select="count(allele)"/>
    <xsl:text> </xsl:text>
   </xsl:if>
  </xsl:for-each>

  <xsl:call-template name="newline"/>

  <xsl:for-each select="$nodes">

   <xsl:call-template name="append-pad">
    <xsl:with-param name="padVar">
     <xsl:value-of select="populationdata/popname"/>
    </xsl:with-param>
    <xsl:with-param name="length" select="9"/>
   </xsl:call-template>
   <xsl:text> </xsl:text>
   
   <xsl:for-each select="locus">
    <xsl:variable name="curlocus" select="@name"/>
    <xsl:variable name="cur-allele-list" select="allelecounts/allele"/>
    
    <xsl:for-each select="$all-allele-list/locus[@name=$curlocus]/allele">
     <xsl:variable name="allelename" select="."/>
     <xsl:choose>
      <xsl:when test="$cur-allele-list[@name=$allelename]">
       <xsl:value-of select="normalize-space($cur-allele-list[@name=$allelename]/frequency)"/>
      </xsl:when>
      <xsl:otherwise>0.00000</xsl:otherwise>
     </xsl:choose>
     <xsl:text> </xsl:text>
    </xsl:for-each>
   </xsl:for-each>
   <xsl:call-template name="newline"/>
  </xsl:for-each>
 
 </xsl:template>
 
 <xsl:template name="line-start">
  <xsl:param name="popnode"/>
  
  <xsl:call-template name="output-field">
   <xsl:with-param name="node" select="translate($popnode/popname, ' ', '-')"/>
  </xsl:call-template>
 
  <xsl:call-template name="output-field">
   <xsl:with-param name="node" select="translate($popnode/ethnic, ' ', '-')"/>
  </xsl:call-template>

  <!-- apply short form of regions as defined in lookup table -->
  <xsl:call-template name="output-field">
   <xsl:with-param name="node" select="$region-order[@long=translate($popnode/contin, ' ', '-')]"/>
  </xsl:call-template>

  <xsl:call-template name="output-field">
   <xsl:with-param name="node" select="translate($popnode/latit, ' ', '_')"/>
  </xsl:call-template>

  <xsl:call-template name="output-field">
   <xsl:with-param name="node" select="translate($popnode/longit, ' ', '_')"/>
  </xsl:call-template>

  <xsl:call-template name="output-field">
   <xsl:with-param name="node" select="translate($popnode/complex, ' ', '_')"/>
  </xsl:call-template>

 </xsl:template>

 <xsl:template name="gen-lines">
  <xsl:param name="nodes"/>
  <xsl:param name="type" select="'1'"/>
  <xsl:param name="pairwise" select="1"/>

  <xsl:for-each select="$nodes">

   <xsl:choose>
    <xsl:when test="$type='1-locus-summary'">

     <xsl:call-template name="line-start">
      <xsl:with-param name="popnode" select="../populationdata"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="translate(@name, '*', '')"/>
     </xsl:call-template>

     <xsl:choose>
      <xsl:when test="allelecounts/allelecount">
       <xsl:value-of select="allelecounts/allelecount"/>
      </xsl:when>
      <xsl:otherwise>0</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>

     <xsl:choose>
      <xsl:when test="allelecounts/distinctalleles">
       <xsl:value-of select="allelecounts/distinctalleles"/>
      </xsl:when>
      <xsl:otherwise>0</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosity/pvalue/lower"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosity/pvalue/upper"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosity/normdev"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="hardyweinbergGuoThompson/pvalue"/>
     </xsl:call-template>
     
     <xsl:choose>
      <!--complete -->
      <xsl:when
       test="hardyweinberg/lumped/@role='no-rare-genotypes' and 
       hardyweinberg/common!=''">
       <xsl:value-of select="hardyweinberg/common/pvalue"/>
      </xsl:when>
      <!-- common + lumped -->
      <xsl:when test="hardyweinberg/lumped!='' and 
       hardyweinberg/common!=''">
       <xsl:value-of select="hardyweinberg/common/pvalue"/>
      </xsl:when>
      <!-- common -->
      <xsl:when test="hardyweinberg/common!=''">
       <xsl:value-of select="hardyweinberg/common/pvalue"/>
      </xsl:when>

      <!-- if either no-common-genotypes or too-many-parameters is found -->
      <!-- output the role attribute rather than a N/A '****' -->
      
      <xsl:when test="hardyweinberg/common[@role='no-common-genotypes' or @role='too-many-parameters']">
       <xsl:value-of select="hardyweinberg/common/@role"/>
      </xsl:when>

      <xsl:otherwise>****</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinberg/homozygotes/pvalue"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinberg/heterozygotes/pvalue"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="hardyweinbergGuoThompsonArlequin/pvalue"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinbergGuoThompsonArlequin/stddev"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinbergGuoThompsonArlequin/exp-hetero"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinbergGuoThompsonArlequin/obs-hetero"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/meanHomozygosity"/>
     </xsl:call-template>
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/probHomozygosity"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/varHomozygosity"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/probEwens"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="count(hardyweinberg/genotypetable/genotype[chisq/@role!='not-calculated'])"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="count(hardyweinberg/genotypetable/genotype/pvalue[. &lt;= 0.05])"/>
     </xsl:call-template>

     <xsl:call-template name="newline"/>

    </xsl:when>

    <xsl:when test="$type='1-locus-allele'">

     <xsl:variable name="curr-line-start">
      <xsl:call-template name="line-start">
       <xsl:with-param name="popnode" select="../populationdata"/>
      </xsl:call-template>
     </xsl:variable>

     <xsl:for-each select="allelecounts/allele">
      <xsl:value-of select="$curr-line-start"/>

      <xsl:value-of select="../../@name"/>
      <xsl:text>&#09;</xsl:text>

      <xsl:value-of select="@name"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="frequency"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="count"/>
      <xsl:call-template name="newline"/>
     </xsl:for-each>
    </xsl:when>

    <xsl:when test="$type='multi-locus-summary'">

     <!-- only attempt to print summary data  if haplotype est. converged -->

     <xsl:if test="haplotypefreq/condition/@role='converged'">

      <xsl:call-template name="line-start">
       <xsl:with-param name="popnode" select="../../populationdata" />
      </xsl:call-template>
      
      <xsl:call-template name="output-field">
       <xsl:with-param name="node"
	select="number(individcount[@role='after-filtering']) * 2"/>
      </xsl:call-template>
      
      <!-- make sure locus1 and locus2 are always in map order -->
      <xsl:for-each select="str:tokenize(@loci, ':')">
       <xsl:sort select="$map-order[.=current()]/@order" data-type="number"/>
       <xsl:value-of select="." />
       <xsl:text>&#09;</xsl:text>
      </xsl:for-each>
      
      <xsl:if test="$pairwise=1">
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/dprime"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/wn"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/q/chisq"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/q/dof"/>
       </xsl:call-template>     
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="permutationSummary/pvalue"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="permutationSummary/lr"/>
       </xsl:call-template>
       
      </xsl:if>
      
      <xsl:call-template name="newline"/>
      
     </xsl:if>
     
    </xsl:when>
    
    <xsl:when test="$type='multi-locus-haplo'">

     <!-- print out message if haplotype estimation failed to converge -->
     <xsl:message>
      <xsl:if test="contains(haplotypefreq/loginfo, 'Percent of iterations with error_flag = 0:   0.000')">
       <xsl:text>Problem with convergence of haplotype </xsl:text>
       <xsl:value-of select="@loci"/> 
       <xsl:text> in file: </xsl:text>
       <xsl:value-of select="../../filename"/>
       <xsl:call-template name="newline"/>
       <xsl:value-of select="substring-before(haplotypefreq/loginfo, '--- Codes for error_flag')"/>
      </xsl:if>
     </xsl:message>

     <!-- only attempt to print haplotypes if converged -->
     <xsl:if test="haplotypefreq/condition/@role='converged'">
     
      <xsl:variable name="curr-line-start">
       <xsl:call-template name="line-start">
	<xsl:with-param name="popnode" select="../../populationdata"/>
       </xsl:call-template>

       <!-- make sure locus1 and locus2 are always in map order -->
       <xsl:for-each select="str:tokenize(@loci, ':')">
	<xsl:sort select="$map-order[.=current()]/@order" data-type="number"/>
	<xsl:value-of select="." />
	<xsl:if test="position()!=last()">
	 <xsl:text>:</xsl:text>
	</xsl:if>
       </xsl:for-each>
       
       <xsl:text>&#09;</xsl:text>
       
      </xsl:variable>
      
      
      <xsl:for-each select="haplotypefreq/haplotype">
       
       <xsl:value-of select="$curr-line-start"/>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="@name"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="frequency"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="numCopies"/>
       </xsl:call-template>
       
       <xsl:if test="$pairwise=1">
	
	<xsl:variable name="first">
	 <xsl:value-of select="substring-before(@name, ':')"/>
	 <xsl:text>:</xsl:text>
	</xsl:variable>
	<xsl:variable name="second">
	 <xsl:value-of select="substring-after(@name, ':')"/>
	</xsl:variable>
       
	<xsl:variable name="pair"
	 select="../../linkagediseq/loci[1]/allelepair[@first=$first and
	 @second=$second]"/>
	
	<xsl:call-template name="output-field">
	 <xsl:with-param name="node" select="$pair/norm_dij"/>
	</xsl:call-template>
	
	<xsl:call-template name="output-field">
	 <xsl:with-param name="node" select="$pair/chisq"/>
	</xsl:call-template>
	
       </xsl:if>

       <xsl:call-template name="newline"/>
       
      </xsl:for-each>

     </xsl:if>

    </xsl:when>

   </xsl:choose>
   
  </xsl:for-each>
 </xsl:template>

 <xsl:template match="/">


  <xsl:choose>

   <xsl:when test="element-available('exsl:document')">

    <exsl:document href="1-locus-summary.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:value-of select="$header-line-start"/><xsl:text>locus&#09;n.gametes&#09;k&#09;f.pval.lower&#09;f.pval.upper&#09;fnd.lookup&#09;gt.pval&#09;hw.chisq.pval&#09;hw.homo.chisq.pval&#09;hw.het.chisq.pval&#09;gt.arl.pval&#09;gt.arl.pval.sd&#09;gt.arl.exp.het&#09;gt.arl.obs.het&#09;f.slatkin.exp&#09;f.slatkin.pval&#09;f.slatkin.var&#09;ewens.pval&#09;n.common.genos&#09;n.common.genos.sig</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes" select="/meta/dataanalysis/locus"/>
      <xsl:with-param name="type" select="'1-locus-summary'"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="1-locus-allele.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:value-of select="$header-line-start"/><xsl:text>locus&#09;allele&#09;allele.freq&#09;allele.count</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes" select="/meta/dataanalysis/locus"/>
      <xsl:with-param name="type" select="'1-locus-allele'"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="2-locus-summary.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:value-of select="$header-line-start"/><xsl:text>n.gametes&#09;locus1&#09;locus2&#09;ld.dprime&#09;ld.wn&#09;q.chisq&#09;q.df&#09;lrt.pval&#09;lrt.z</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes"
       select="/meta/dataanalysis/emhaplofreq/group[(@mode='all-pairwise-ld-with-permu' or @mode='all-pairwise-ld-no-permu') and @role!='no-data']"/>
      <xsl:with-param name="type" select="'multi-locus-summary'"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="2-locus-haplo.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:value-of select="$header-line-start"/><xsl:text>locus&#09;allele&#09;allele.freq&#09;allele.count&#09;ld.dprime&#09;ld.chisq</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes"
      select="/meta/dataanalysis/emhaplofreq/group[(@mode='all-pairwise-ld-with-permu' or @mode='all-pairwise-ld-no-permu') and @role!='no-data']"/>
      <xsl:with-param name="type" select="'multi-locus-haplo'"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="3-locus-summary.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:value-of select="$header-line-start"/><xsl:text>n.gametes&#09;locus1&#09;locus2&#09;locus3</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes"
       select="/meta/dataanalysis/emhaplofreq/group[(string-length(@loci) - string-length(translate(@loci, ':', '')))=2 and @role!='no-data']"/>
      <xsl:with-param name="type" select="'multi-locus-summary'"/>
      <xsl:with-param name="pairwise" select="0"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="3-locus-haplo.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:value-of select="$header-line-start"/><xsl:text>locus&#09;allele&#09;allele.freq&#09;allele.count</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes"
      select="/meta/dataanalysis/emhaplofreq/group[(string-length(@loci) - string-length(translate(@loci, ':', '')))=2 and @role!='no-data']"/>
      <xsl:with-param name="type" select="'multi-locus-haplo'"/>
      <xsl:with-param name="pairwise" select="0"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="4-locus-summary.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:value-of select="$header-line-start"/><xsl:text>n.gametes&#09;locus1&#09;locus2&#09;locus3&#09;locus4</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes"
       select="/meta/dataanalysis/emhaplofreq/group[(string-length(@loci) - string-length(translate(@loci, ':', '')))=3 and @role!='no-data']"/>
      <xsl:with-param name="type" select="'multi-locus-summary'"/>
      <xsl:with-param name="pairwise" select="0"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="4-locus-haplo.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:value-of select="$header-line-start"/><xsl:text>locus&#09;allele&#09;allele.freq&#09;allele.count</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes"
      select="/meta/dataanalysis/emhaplofreq/group[(string-length(@loci) - string-length(translate(@loci, ':', '')))=3 and @role!='no-data']"/>
      <xsl:with-param name="type" select="'multi-locus-haplo'"/>
      <xsl:with-param name="pairwise" select="0"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="phylip.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:call-template name="phylip-lines">
      <xsl:with-param name="nodes" select="/meta/dataanalysis"/>
     </xsl:call-template>
    
    </exsl:document>


    </xsl:when>

   <xsl:otherwise>
    <xsl:message>needs a processor that understands exsl elements, see http://exsl.org/
    </xsl:message>
   </xsl:otherwise>
  </xsl:choose>

 </xsl:template>

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
